"""
Sida 5: Begrepp
En enkel ordlista med de viktigaste begreppen för fastighetsbolag.
Lägg till ett nytt begrepp genom att kopiera ett av blocken i listan.
"""
from html import escape

import streamlit as st

import stil

stil.sidhuvud("ORD", "Begrepp", "Ordlista för fastighetsaktier")

BEGREPP = [
    {
        "namn": "Förvaltningsresultat",
        "kort": "Income from property management",
        "forklaring": "Det bolaget tjänar på sin vardagliga verksamhet: hyresintäkter minus "
                      "driftkostnader, administration och räntor. Värdeförändringar på fastigheterna "
                      "och skatt räknas inte med. Därför visar det hur mycket pengar verksamheten "
                      "faktiskt ger, och det styr ofta hur stor utdelningen blir.",
        "exempel": "Hyror 1 000 mkr − fastighetskostnader 300 − administration 50 − räntor 250 "
                   "= förvaltningsresultat 400 mkr.",
    },
    {
        "namn": "NAV",
        "kort": "Substansvärde · Net Asset Value",
        "forklaring": "Vad bolaget är värt enligt balansräkningen: fastigheternas marknadsvärde plus "
                      "övriga tillgångar minus skulderna. Fastighetsbolag redovisar oftast "
                      "långsiktigt substansvärde, där bland annat uppskjuten skatt inte räknas "
                      "som skuld. Delar man med antalet aktier får man NAV per aktie.",
        "exempel": "Fastigheter 10 000 mkr − skulder 5 500 mkr = 4 500 mkr. "
                   "Med 50 miljoner aktier blir NAV 90 kr per aktie.",
    },
    {
        "namn": "P/NAV",
        "kort": "Price / NAV",
        "forklaring": "Aktiekursen delad med NAV per aktie. Under 1,0 handlas aktien till rabatt mot "
                      "substansvärdet, över 1,0 till premie. En rabatt kan betyda att aktien är billig, "
                      "eller att marknaden tror att fastigheterna är värderade för högt.",
        "exempel": "Kurs 72 kr och NAV 90 kr ger P/NAV 0,80, alltså 20 % rabatt.",
    },
    {
        "namn": "Belåningsgrad",
        "kort": "LTV · Loan to value",
        "forklaring": "Hur stor del av fastigheternas värde som är lånat: räntebärande skulder (ofta "
                      "minus kassan) delat med fastigheternas värde. Högre belåning betyder mer risk, "
                      "eftersom små fall i fastighetsvärdet då slår hårt mot ägarnas del. Många bolag "
                      "har som mål att ligga under 40–50 %.",
        "exempel": "Lån 5 500 mkr och fastigheter 10 000 mkr ger belåningsgrad 55 %.",
    },
    {
        "namn": "Räntetäckningsgrad",
        "kort": "ICR · Interest coverage ratio",
        "forklaring": "Hur många gånger resultatet räcker till att betala räntorna: förvaltningsresultat "
                      "plus räntekostnader, delat med räntekostnaderna. Ju högre desto säkrare. Under "
                      "1,0 räcker resultatet inte ens till räntorna, och långivare kräver ofta minst "
                      "omkring 1,5 gånger.",
        "exempel": "(400 + 250) ÷ 250 = 2,6 gånger.",
    },
    {
        "namn": "Direktavkastning",
        "kort": "Dividend yield · Yield",
        "forklaring": "Ordet används på två sätt. För aktien är det utdelningen delad med kursen, och "
                      "det är den som visas i appen. För en fastighet är det driftnettot (hyror minus "
                      "driftkostnader) delat med fastighetens värde. När räntan stiger kräver köpare "
                      "högre direktavkastning, och då sjunker fastighetens värde.",
        "exempel": "Aktie: utdelning 3 kr ÷ kurs 100 kr = 3 %. Fastighet: driftnetto 50 mkr ÷ 5 % "
                   "= värde 1 000 mkr, men ÷ 5,5 % = bara 909 mkr.",
    },
    {
        "namn": "Baspunkt",
        "kort": "bp · punkt",
        "forklaring": "En hundradels procentenhet: 1 baspunkt = 0,01 procentenheter och 100 baspunkter "
                      "= 1 procentenhet. Används för små ränteförändringar, så att man inte blandar "
                      "ihop procent och procentenheter.",
        "exempel": "Räntan går från 2,41 % till 2,66 %: den har stigit 25 baspunkter.",
    },
]

# --- Sökruta --------------------------------------------------------------------------
valruta, _ = st.columns([1, 2])
with valruta:
    sok = st.text_input("Sök begrepp", placeholder="t.ex. NAV eller belåning")

# Behåll bara begrepp där söktexten finns i namnet, kortnamnet eller förklaringen.
sok = sok.strip().lower()
traffar = [b for b in BEGREPP
           if sok in (b["namn"] + " " + b["kort"] + " " + b["forklaring"]).lower()]

stil.rubrik("Ordlista", f"{len(traffar)} av {len(BEGREPP)} begrepp")
if not traffar:
    stil.fotnot("Inget begrepp matchar sökningen.")

for b in traffar:
    st.html(f"""
    <div class="ft-begrepp">
      <div class="ft-begrepp-namn">{escape(b["namn"])}<span>{escape(b["kort"])}</span></div>
      <div class="ft-begrepp-text">
        {escape(b["forklaring"])}
        <div class="ft-begrepp-exempel"><b>Exempel:</b> {escape(b["exempel"])}</div>
      </div>
    </div>""")
