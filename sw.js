/* Snabbmatte offline: sparar appen och allt den behöver på enheten.
   Uppgifterna skapas av appen själv, så när filerna här finns sparade
   går det att träna obegränsat utan internet. */
const CACHE = 'snabbmatte-v1';
const KATEX = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/';
const KATEX_FONTS = ['AMS-Regular','Caligraphic-Bold','Caligraphic-Regular','Fraktur-Bold','Fraktur-Regular','Main-Bold','Main-BoldItalic',
  'Main-Italic','Main-Regular','Math-BoldItalic','Math-Italic','SansSerif-Bold','SansSerif-Italic','SansSerif-Regular','Script-Regular',
  'Size1-Regular','Size2-Regular','Size3-Regular','Size4-Regular','Typewriter-Regular'];
const GFONTS = 'https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&family=Inter:wght@500;600;700;800&display=swap';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];
const EXTERNAL = [KATEX + 'katex.min.js', KATEX + 'katex.min.css', ...KATEX_FONTS.map(f => KATEX + 'fonts/KaTeX_' + f + '.woff2'),
  'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.117.2/dist/umd/supabase.js', GFONTS];

async function store(cache, url) {
  const res = await fetch(url, { mode: url.startsWith('http') ? 'cors' : 'same-origin', cache: 'reload' });
  if (!res.ok) throw new Error(url);
  await cache.put(url, res.clone());
  return res;
}
// Laddar ned allt. Typsnittsfilerna från Google står i deras CSS, så den läses först.
async function precache(progress = () => {}) {
  const cache = await caches.open(CACHE);
  await Promise.all(SHELL.map(u => store(cache, u)));
  let urls = EXTERNAL.slice(), fonts = [];
  try {
    const css = await (await store(cache, GFONTS)).text();
    fonts = [...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)].map(m => m[1]);
  } catch (e) {}
  urls = urls.filter(u => u !== GFONTS).concat(fonts);
  const total = SHELL.length + 1 + urls.length; let done = SHELL.length + 1, failed = 0;
  progress(done, total);
  await Promise.all(urls.map(u => store(cache, u).catch(() => failed++).then(() => progress(++done, total))));
  return { total, failed };
}
async function status() {
  const cache = await caches.open(CACHE);
  const need = SHELL.concat(EXTERNAL);
  const have = await Promise.all(need.map(u => cache.match(u)));
  return { ready: have.every(Boolean), have: have.filter(Boolean).length, total: need.length };
}

self.addEventListener('install', e => {
  e.waitUntil(precache().catch(() => {}).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('message', e => {
  const port = e.ports[0]; if (!port) return;
  if (e.data === 'status') status().then(s => port.postMessage({ type: 'status', ...s }));
  if (e.data === 'precache') precache((done, total) => port.postMessage({ type: 'progress', done, total }))
    .then(r => status().then(s => port.postMessage({ type: 'done', failed: r.failed, ...s })))
    .catch(() => port.postMessage({ type: 'error' }));
});

const timeout = ms => new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms));
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.hostname.endsWith('.supabase.co')) return;   // inloggning och molnsparning går alltid direkt
  if (url.origin === location.origin) {
    // Appen själv: hämta den nyaste när det finns nät, annars den sparade
    e.respondWith((async () => {
      const cache = await caches.open(CACHE);
      try {
        const res = await Promise.race([fetch(req), timeout(4000)]);
        if (res.ok) cache.put(req.mode === 'navigate' ? './index.html' : req, res.clone());
        return res;
      } catch (err) {
        return (await cache.match(req, { ignoreSearch: true })) || (req.mode === 'navigate' && await cache.match('./index.html')) || Response.error();
      }
    })());
    return;
  }
  // Bibliotek och typsnitt har fasta versioner: ta den sparade direkt
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const hit = await cache.match(req.url);
    if (hit) return hit;
    const res = await fetch(req);
    if (res.ok || res.type === 'opaque') cache.put(req.url, res.clone());
    return res;
  })());
});
