# Snabbmatte – Matte 2

En mobilvänlig webbapp för att träna snabb huvudräkning i Matte 2, kapitlet *Algebra och icke-linjära modeller*.

- Hela appen ligger i `index.html` (HTML, CSS och JavaScript, ingen byggprocess).
- Testerna finns i `tests.html`. Öppna den via en webbserver, till exempel GitHub Pages: `…/tests.html`.
- Framsteg sparas i webbläsarens localStorage. Med konto sparas de också i molnet via Supabase, se `KONTO.md`.
- **Kapitel 2 i boken** följer bokens innehållsförteckning, 2.1–2.5 plus Sammanfattning, Testa dig själv och Blandade övningar. Avsnitten och vilka uppgiftstyper de använder står i `BOOK` i `index.html`.
- **Tidspress** är av som standard och slås på från startsidan eller boken. Uppgifter med `noTime`, miniräknaruppgifter och utmaningar har aldrig klocka. Slutbossen har det alltid.
- **Förklaringen** visas först när man trycker på knappen efter ett svar. Den går steg för steg och har en Förstår inte-knapp med enklare nivåer.
