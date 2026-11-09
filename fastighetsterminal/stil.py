"""
Stil – allt som har med utseendet att göra.

Filen innehåller två delar:
1. CSS: koden som bestämmer färger, typsnitt och storlekar i webbläsaren.
2. Små ritfunktioner (sidhuvud, ruta, tabell, panel …) som sidorna i
   mappen sidor/ anropar. Då ser alla sidor likadana ut, och du ändrar
   utseendet på ett enda ställe.

Ritfunktionerna bygger lite HTML (webbsidornas språk) och visar den med
st.html. Text som kommer från datafilerna skickas genom escape(), som gör
om tecken som < och > så att de visas som text i stället för att tolkas
som HTML.
"""
from datetime import date
from html import escape

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# 1. CSS – färger och typsnitt
# ---------------------------------------------------------------------------
# Färgerna ligger som variabler högst upp (--ft-orange osv.), så är de lätta
# att ändra. "ft" står för fastighetsterminal.
#
# Typsnitten (IBM Plex Sans och IBM Plex Mono) laddas i .streamlit/config.toml.
CSS = """
<style>
:root {
  --ft-svart:  #000000;
  --ft-panel:  #0c0e11;   /* mörkgrå bakgrund i rutor */
  --ft-panel2: #15181d;   /* lite ljusare grå, t.ex. tabellrubriker */
  --ft-linje:  #2a2f37;   /* tunna linjer */
  --ft-text:   #e8e8e8;
  --ft-dov:    #8d95a0;   /* dämpad grå text */
  --ft-orange: #ff9f1c;   /* accentfärgen */
  --ft-rodbar: #7a1416;   /* mörkröd rad i sidhuvudet */
  --ft-gron:   #3ddc84;   /* upp */
  --ft-rod:    #ff5b55;   /* ner */
  --ft-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --ft-sans: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
}

/* ---------- Streamlits egna delar ---------- */
/* Lite mindre luft mellan delarna, så att mer får plats. */
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] { gap: 0.75rem; }
/* Rubriker på inmatningsrutor: små, orange och i versaler. */
[data-testid="stWidgetLabel"] p {
  font-family: var(--ft-mono); font-size: 12px; color: var(--ft-orange);
  text-transform: uppercase; letter-spacing: .05em;
}
/* Menyn i sidofältet: vald sida får en orange kant. */
[data-testid="stSidebarNavLink"] p { font-family: var(--ft-mono); font-size: 14px; }
[data-testid="stSidebarNavLink"][aria-current="page"] { box-shadow: inset 3px 0 0 var(--ft-orange); }

/* ---------- Färgklasser ---------- */
.upp    { color: var(--ft-gron); }
.ner    { color: var(--ft-rod); }
.still  { color: var(--ft-text); }
.dov    { color: var(--ft-dov); }
.orange { color: var(--ft-orange); }

/* ---------- Sidhuvud ---------- */
.ft-huvud { display: flex; flex-wrap: wrap; font-family: var(--ft-mono); }
.ft-huvud-kod {
  background: var(--ft-orange); color: #000; padding: 6px 14px;
  font-size: 20px; font-weight: 600; min-width: 220px;
}
.ft-huvud-kod b { font-weight: 600; margin-right: 10px; opacity: .65; }
.ft-huvud-rad {
  flex: 1; display: flex; flex-wrap: wrap; align-items: center;
  justify-content: space-between; gap: 6px 16px;
  background: var(--ft-rodbar); color: #fff; padding: 6px 14px; font-size: 14px;
}
.ft-huvud-hoger { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; white-space: nowrap; }
.ft-exempel {
  background: #000; color: var(--ft-orange); border: 1px solid var(--ft-orange);
  padding: 1px 7px; font-size: 12px; font-weight: 600; letter-spacing: .04em;
}

/* ---------- Tickerremsan ---------- */
.ft-ticker {
  overflow: hidden; white-space: nowrap; background: var(--ft-panel);
  border-top: 1px solid var(--ft-linje); border-bottom: 1px solid var(--ft-linje);
  font-family: var(--ft-mono); font-size: 13px; font-variant-numeric: tabular-nums;
}
.ft-ticker-spar { display: inline-block; padding: 5px 0; animation: ft-rulla 70s linear infinite; }
.ft-ticker:hover .ft-ticker-spar { animation-play-state: paused; }
.ft-tickerpost { padding-right: 32px; }
.ft-tickerpost b { color: var(--ft-orange); font-weight: 500; margin-right: 6px; }
@keyframes ft-rulla { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) {
  .ft-ticker { overflow-x: auto; }
  .ft-ticker-spar { animation: none; }
}

/* ---------- Rubrikrad ovanför tabeller ---------- */
.ft-rubrik {
  display: flex; flex-wrap: wrap; gap: 2px 16px; justify-content: space-between; align-items: baseline;
  border-bottom: 1px solid var(--ft-orange); padding: 2px 0 4px;
  font-family: var(--ft-mono); font-size: 13px; text-transform: uppercase;
  letter-spacing: .05em; color: var(--ft-orange);
}
.ft-rubrik .dov { text-transform: none; letter-spacing: 0; }

/* ---------- Rutor med ett stort värde ---------- */
.ft-ruta { background: var(--ft-panel); border: 1px solid var(--ft-linje); font-family: var(--ft-mono); }
.ft-ruta-titel {
  display: flex; justify-content: space-between; align-items: center;
  background: var(--ft-panel2); border-bottom: 1px solid var(--ft-linje);
  padding: 4px 12px; font-size: 12px; color: var(--ft-orange);
  text-transform: uppercase; letter-spacing: .05em;
}
.ft-ruta-titel .ft-exempel { font-size: 10px; padding: 0 5px; }
.ft-ruta-innehall { padding: 8px 12px 10px; font-variant-numeric: tabular-nums; }
.ft-ruta-varde { font-size: 32px; font-weight: 500; color: #fff; line-height: 1.15; }
.ft-ruta-varde .ft-enhet { font-size: 15px; color: var(--ft-dov); margin-left: 8px; }
.ft-ruta-forandring { font-size: 14px; margin-top: 2px; }

/* ---------- Små siffertavlor (prediktionsloggen) ---------- */
.ft-siffra { background: var(--ft-panel); border: 1px solid var(--ft-linje); padding: 6px 12px; font-family: var(--ft-mono); }
.ft-siffra-titel { font-size: 11px; color: var(--ft-dov); text-transform: uppercase; letter-spacing: .05em; }
.ft-siffra-varde { font-size: 22px; color: #fff; font-variant-numeric: tabular-nums; }

/* ---------- Tabeller ---------- */
.ft-tabell { overflow-x: auto; border: 1px solid var(--ft-linje); }
.ft-tabell table { width: 100%; border-collapse: collapse; font-size: 13.5px; color: var(--ft-text); }
.ft-tabell th {
  background: var(--ft-panel2); color: var(--ft-orange); font-family: var(--ft-mono);
  font-weight: 500; font-size: 12px; text-transform: uppercase; letter-spacing: .04em;
  text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--ft-linje); white-space: nowrap;
}
.ft-tabell td { padding: 5px 10px; border-bottom: 1px solid #1a1e24; white-space: nowrap; font-family: var(--ft-sans); }
.ft-tabell tbody tr:nth-child(even) { background: #07080a; }
.ft-tabell tbody tr:hover { background: #1c2027; }
.ft-tabell tfoot td { border-top: 1px solid var(--ft-orange); border-bottom: none; color: var(--ft-dov); font-weight: 600; }
/* Siffror: monospace och högerställda, så att decimalerna hamnar under varandra. */
.ft-tabell .num  { text-align: right; font-family: var(--ft-mono); font-variant-numeric: tabular-nums; }
.ft-tabell .mono { font-family: var(--ft-mono); font-variant-numeric: tabular-nums; }
/* Lång text får radbrytas. */
.ft-tabell .lang { white-space: normal; min-width: 200px; max-width: 360px; line-height: 1.4; }

/* ---------- Bolagssidan ---------- */
.ft-kursrad {
  display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 18px;
  font-family: var(--ft-mono); padding: 4px 0 2px; font-variant-numeric: tabular-nums;
}
.ft-kursrad-ticker { color: var(--ft-orange); font-size: 22px; font-weight: 600; }
.ft-kursrad-namn   { color: #fff; font-size: 18px; font-family: var(--ft-sans); }
.ft-kursrad-kurs   { color: #fff; font-size: 26px; font-weight: 500; }
.ft-kursrad-forandring { font-size: 16px; }

.ft-panel { background: var(--ft-panel); border: 1px solid var(--ft-linje); overflow-x: auto; }
.ft-panel table { width: 100%; border-collapse: collapse; font-size: 13.5px; }
.ft-panel th {
  font-family: var(--ft-mono); font-weight: 500; font-size: 11px; color: var(--ft-dov);
  text-transform: uppercase; text-align: right; padding: 4px 8px; white-space: nowrap;
}
.ft-panel th:first-child { text-align: left; color: var(--ft-orange); font-size: 12px; letter-spacing: .05em; }
.ft-panel thead tr { background: var(--ft-panel2); }
.ft-panel th:first-child, .ft-panel td:first-child { padding-left: 12px; }
.ft-panel td { padding: 5px 8px; border-top: 1px solid #1a1e24; color: var(--ft-text); }
.ft-panel td.num { text-align: right; font-family: var(--ft-mono); font-variant-numeric: tabular-nums; color: #fff; white-space: nowrap; }
.ft-panel td.num.dov { color: var(--ft-dov); }

/* ---------- Platshållare för grafer ---------- */
.ft-platshallare {
  position: relative; border: 1px dashed #3a414b; font-family: var(--ft-mono);
  background-color: var(--ft-panel);
  background-image:
    linear-gradient(#161a20 1px, transparent 1px),
    linear-gradient(90deg, #161a20 1px, transparent 1px);
  background-size: 100% 40px, 80px 100%;
  display: flex; align-items: center; justify-content: center; text-align: center;
}
.ft-platshallare-titel {
  position: absolute; top: 0; left: 0; right: 0; padding: 4px 12px;
  background: var(--ft-panel2); border-bottom: 1px solid var(--ft-linje);
  color: var(--ft-orange); font-size: 12px; text-transform: uppercase; letter-spacing: .05em; text-align: left;
}
.ft-platshallare-text { color: var(--ft-dov); font-size: 13px; padding: 40px 24px 16px; max-width: 520px; }
.ft-platshallare-text b { display: block; color: var(--ft-text); letter-spacing: .1em; margin-bottom: 6px; }

/* ---------- Textrutor och fotnoter ---------- */
.ft-text { background: var(--ft-panel); border: 1px solid var(--ft-linje); border-left: 3px solid var(--ft-orange); padding: 10px 14px; font-family: var(--ft-sans); font-size: 14.5px; line-height: 1.55; }
.ft-text ol, .ft-text ul { margin: 4px 0 0; padding-left: 20px; }
.ft-text li { margin-bottom: 4px; }
.ft-fotnot { font-family: var(--ft-sans); font-size: 12.5px; color: var(--ft-dov); line-height: 1.5; }

/* ---------- Begrepp ---------- */
.ft-begrepp { display: grid; grid-template-columns: 230px 1fr; border-bottom: 1px solid var(--ft-linje); padding: 12px 0; gap: 4px 20px; }
.ft-begrepp-namn { font-family: var(--ft-mono); color: var(--ft-orange); font-size: 15px; font-weight: 600; }
.ft-begrepp-namn span { display: block; color: var(--ft-dov); font-size: 12px; font-weight: 400; margin-top: 2px; }
.ft-begrepp-text { font-family: var(--ft-sans); font-size: 15px; line-height: 1.55; color: var(--ft-text); }
.ft-begrepp-exempel { margin-top: 6px; font-family: var(--ft-mono); font-size: 13px; color: #cfd3d8; background: var(--ft-panel); border-left: 2px solid var(--ft-linje); padding: 4px 10px; }
.ft-begrepp-exempel b { color: var(--ft-orange); font-weight: 500; }

/* ---------- Sidofältet ---------- */
.ft-sidoinfo { font-family: var(--ft-mono); font-size: 12px; color: var(--ft-dov); border-top: 1px solid var(--ft-linje); padding-top: 10px; line-height: 1.8; }
.ft-sidoinfo .ft-logga { color: var(--ft-orange); font-weight: 600; font-size: 14px; letter-spacing: .08em; line-height: 1.3; margin-bottom: 6px; }
.ft-sidoinfo span { color: var(--ft-text); }

/* ---------- Smal skärm (mobil) ---------- */
@media (max-width: 640px) {
  .ft-huvud-kod { min-width: 0; flex: 1 1 100%; }
  .ft-begrepp { grid-template-columns: 1fr; }
  .ft-ruta-varde { font-size: 26px; }
}
</style>
"""


def ladda_stil():
    """Lägger in CSS:en på sidan. Anropas en gång, i app.py."""
    st.html(CSS)


# ---------------------------------------------------------------------------
# 2. Formatering av tal – svenskt format: 1 284,37
# ---------------------------------------------------------------------------
def tal(varde, decimaler=2, plustecken=False):
    """Gör om ett tal till text med svenskt format, t.ex. 1 284,37.

    plustecken=True sätter + framför positiva tal (bra för förändringar).
    Saknas värdet visas ett streck.
    """
    if varde is None or pd.isna(varde):
        return "–"
    tecken = "+" if plustecken and varde != 0 else ""
    text = f"{varde:{tecken},.{decimaler}f}"  # Python ger t.ex. "1,284.37"
    # Byt till svenska tecken.   är ett mellanslag som aldrig radbryts.
    return text.replace(",", " ").replace(".", ",")


def riktning(varde):
    """Ger CSS-klassen 'upp' (grönt), 'ner' (rött) eller 'still' (vitt)."""
    if pd.isna(varde) or varde == 0:
        return "still"
    return "upp" if varde > 0 else "ner"


def forandring(varde, enhet="%"):
    """En färgad förändring, t.ex. +1,24 % i grönt eller -3 bp i rött."""
    if enhet == "bp":  # baspunkter visas utan decimaler
        text = tal(varde, 0, plustecken=True) + " bp"
    else:
        text = tal(varde, 2, plustecken=True) + " %"
    return f'<span class="{riktning(varde)}">{text}</span>'


def betyg(varde):
    """Betyg 1–5 som prickar: ●●●○○ 3. Saknas betyg visas ett streck."""
    if pd.isna(varde):
        return '<span class="dov">–</span>'
    n = int(varde)
    return f'<span class="orange">{"●" * n}</span><span class="dov">{"○" * (5 - n)}</span> {n}'


def utfall(varde):
    """Utfallet av en prediktion. Tomt utfall betyder att vi väntar."""
    if pd.isna(varde):
        return '<span class="dov">Väntar …</span>'
    return escape(str(varde))


# Hur ett värde ska visas. Nyckeln är formatets namn och värdet är en
# funktion som gör om värdet till text. Sidorna väljer format per kolumn.
FORMAT = {
    "text":       lambda v: escape(str(v)),
    "lang":       lambda v: escape(str(v)),       # lång text som får radbrytas
    "kr":         lambda v: tal(v, 2),            # 142,30
    "kvot":       lambda v: tal(v, 2),            # 0,84
    "procent":    lambda v: tal(v, 1) + " %",     # 44,8 %
    "ggr":        lambda v: tal(v, 1) + " ggr",   # 2,6 ggr
    "mdkr":       lambda v: tal(v, 1) + " mdkr",  # 62,4 mdkr
    "forandring": lambda v: forandring(v, "%"),   # +1,24 % (färgad)
    "datum":      lambda v: v.strftime("%Y-%m-%d"),
    "betyg":      betyg,
    "utfall":     utfall,
}

# Vilken CSS-klass varje format får i tabeller:
# "num" = siffror (monospace, högerställda), "mono" = monospace, "lang" = radbryts.
KLASS = {
    "kr": "num", "kvot": "num", "procent": "num", "ggr": "num", "mdkr": "num",
    "forandring": "num", "datum": "mono", "betyg": "mono",
    "lang": "lang", "utfall": "lang",
}


def formatera(varde, fmt):
    """Visar ett värde med ett av formaten i FORMAT."""
    # Betyg och utfall visar något eget när värdet saknas, övriga visar ett streck.
    if fmt not in ("betyg", "utfall") and pd.isna(varde):
        return '<span class="dov">–</span>'
    return FORMAT[fmt](varde)


# ---------------------------------------------------------------------------
# 3. Byggklossar som sidorna använder
# ---------------------------------------------------------------------------
MANADER = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]


def sidhuvud(kod, titel, beskrivning):
    """Orange-röd rubrikrad högst upp på varje sida, som i terminalen.

    kod  – kort kod för sidan, t.ex. "BEV"
    titel – sidans namn, t.ex. "Översikt"
    """
    idag = date.today()
    datum = f"{idag.day} {MANADER[idag.month - 1]} {idag.year}"
    st.html(f"""
    <div class="ft-huvud">
      <div class="ft-huvud-kod"><b>{escape(kod)}</b>{escape(titel)}</div>
      <div class="ft-huvud-rad">
        <span>{escape(beskrivning)}</span>
        <span class="ft-huvud-hoger">
          <span class="ft-exempel">EXEMPELDATA · PÅHITTADE SIFFROR</span>
          <span>{datum}</span>
        </span>
      </div>
    </div>""")


def tickerremsa(bolag):
    """Rullande remsa med kurserna i bevakningslistan (visas på alla sidor)."""
    poster = "".join(
        f'<span class="ft-tickerpost"><b>{escape(rad.ticker)}</b>'
        f'{tal(rad.kurs)} {forandring(rad.forandring_pct)}</span>'
        for rad in bolag.itertuples()
    )
    # Innehållet läggs in två gånger så att rullningen kan gå runt utan glapp.
    st.html(
        f'<div class="ft-ticker"><div class="ft-ticker-spar">'
        f'<span>{poster}</span><span aria-hidden="true">{poster}</span>'
        f'</div></div>'
    )


def rubrik(text, hoger=""):
    """Tunn orange rubrikrad, t.ex. ovanför en tabell."""
    st.html(f'<div class="ft-rubrik"><span>{escape(text)}</span><span class="dov">{escape(hoger)}</span></div>')


def ruta(serie):
    """Ruta med ett stort värde, t.ex. fastighetsindex eller en ränta.

    'serie' är en rad från marknadstabellen (se datakalla.hamta_marknad)
    med kolumnerna namn, varde, enhet, forandring, forandring_enhet, period.
    """
    rikt = riktning(serie["forandring"])
    pil = {"upp": "▲", "ner": "▼", "still": "■"}[rikt]
    st.html(f"""
    <div class="ft-ruta">
      <div class="ft-ruta-titel">
        <span>{escape(serie["namn"])}</span><span class="ft-exempel">EXEMPEL</span>
      </div>
      <div class="ft-ruta-innehall">
        <div class="ft-ruta-varde">{tal(serie["varde"])}<span class="ft-enhet">{escape(serie["enhet"])}</span></div>
        <div class="ft-ruta-forandring">
          <span class="{rikt}">{pil}</span> {forandring(serie["forandring"], serie["forandring_enhet"])}
          <span class="dov">{escape(serie["period"])}</span>
        </div>
      </div>
    </div>""")


def siffra(titel, varde):
    """Liten tavla med en rubrik och en siffra."""
    st.html(f'<div class="ft-siffra"><div class="ft-siffra-titel">{escape(titel)}</div>'
            f'<div class="ft-siffra-varde">{varde}</div></div>')


def tabell(df, kolumner, fotrad=None):
    """Kompakt tabell i terminalstil.

    df       – tabellen (en pandas DataFrame)
    kolumner – lista med (kolumn i df, rubrik, format), t.ex. ("kurs", "Kurs", "kr").
               Formaten finns i FORMAT ovan.
    fotrad   – valfri sista rad, t.ex. {"bolag": "Snitt", "p_nav": 0.85}.
    """
    huvud = "".join(f'<th class="{KLASS.get(fmt, "")}">{escape(rubrik)}</th>'
                    for _, rubrik, fmt in kolumner)

    rader = []
    for _, rad in df.iterrows():
        celler = "".join(f'<td class="{KLASS.get(fmt, "")}">{formatera(rad[kol], fmt)}</td>'
                         for kol, _, fmt in kolumner)
        rader.append(f"<tr>{celler}</tr>")

    fot = ""
    if fotrad:
        celler = "".join(
            f'<td class="{KLASS.get(fmt, "")}">{formatera(fotrad[kol], fmt) if kol in fotrad else ""}</td>'
            for kol, _, fmt in kolumner)
        fot = f"<tfoot><tr>{celler}</tr></tfoot>"

    st.html(f'<div class="ft-tabell"><table><thead><tr>{huvud}</tr></thead>'
            f'<tbody>{"".join(rader)}</tbody>{fot}</table></div>')


def kursrad(rad):
    """Stor rad med ticker, namn, kurs och förändring (bolagssidan)."""
    st.html(f"""
    <div class="ft-kursrad">
      <span class="ft-kursrad-ticker">{escape(rad["ticker"])}</span>
      <span class="ft-kursrad-namn">{escape(rad["bolag"])}</span>
      <span class="dov">{escape(rad["segment"])}</span>
      <span class="ft-kursrad-kurs">{tal(rad["kurs"])} <span class="dov">SEK</span></span>
      <span class="ft-kursrad-forandring">{forandring(rad["forandring_pct"])}</span>
    </div>""")


def nyckeltalspanel(titel, rader, bolag, snitt):
    """Panel med nyckeltal för ett bolag, jämfört med snittet i listan.

    rader – lista med (namn, kolumn, format, visa_snitt)
    bolag – bolagets rad i bevakningslistan
    snitt – medelvärden för hela listan (visas i kolumnen "Snitt")
    """
    html_rader = "".join(
        f'<tr><td>{escape(namn)}</td>'
        f'<td class="num">{formatera(bolag[kol], fmt)}</td>'
        f'<td class="num dov">{formatera(snitt[kol], fmt) if visa_snitt else "–"}</td></tr>'
        for namn, kol, fmt, visa_snitt in rader
    )
    st.html(f'<div class="ft-panel"><table><thead><tr><th>{escape(titel)}</th>'
            f'<th>Bolaget</th><th>Snitt</th></tr></thead><tbody>{html_rader}</tbody></table></div>')


def platshallare(titel, text, hojd=260):
    """Tom ruta med rutnät som visar var en graf ska ligga senare."""
    st.html(f"""
    <div class="ft-platshallare" style="height:{hojd}px">
      <div class="ft-platshallare-titel">{escape(titel)}</div>
      <div class="ft-platshallare-text"><b>PLATSHÅLLARE</b>{escape(text)}</div>
    </div>""")


def textruta(html):
    """Ruta med förklarande text (får innehålla enkel HTML som <b> och <ol>)."""
    st.html(f'<div class="ft-text">{html}</div>')


def fotnot(text):
    """Liten grå förklaringstext, t.ex. under en tabell."""
    st.html(f'<div class="ft-fotnot">{escape(text)}</div>')


def sidofalt_info():
    """Liten informationsruta längst ner i sidofältet."""
    st.sidebar.html("""
    <div class="ft-sidoinfo">
      <div class="ft-logga">FASTIGHETS-<br>TERMINAL</div>
      <div>LÄGE&nbsp;&nbsp;<span class="orange">EXEMPELDATA</span></div>
      <div>KÄLLA&nbsp;<span>data/*.csv</span></div>
      <div>VER&nbsp;&nbsp;&nbsp;<span>0.1</span></div>
    </div>""")
