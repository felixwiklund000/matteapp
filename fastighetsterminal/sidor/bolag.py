"""
Sida 2: Bolag
Välj ett bolag och se dess nyckeltal (jämfört med snittet i listan),
en platshållare för kursgrafen och bolagets rader i prediktionsloggen.
"""
import streamlit as st

import datakalla
import stil

stil.sidhuvud("BOL", "Bolag", "Nyckeltal för ett bolag i bevakningslistan")

bolag = datakalla.hamta_bevakningslista()

# --- Välj bolag ---------------------------------------------------------------
# Listan visar "TICKER · Namn", men det vi faktiskt väljer är radens nummer.
valruta, _ = st.columns([1, 2])
with valruta:
    radnummer = st.selectbox(
        "Välj bolag",
        bolag.index,
        format_func=lambda i: f"{bolag.loc[i, 'ticker']}  ·  {bolag.loc[i, 'bolag']}",
    )
valt = bolag.loc[radnummer]           # det valda bolagets rad
snitt = bolag.mean(numeric_only=True)  # snittet för hela listan, att jämföra med

stil.kursrad(valt)

# --- Nyckeltal i tre paneler ----------------------------------------------------
# (namn, kolumn i datan, format, visa snitt?)
# Värden "per aktie" går inte att jämföra mellan bolag, så där visas inget snitt.
VARDERING = [
    ("Kurs (kr)", "kurs", "kr", False),
    ("NAV/aktie (kr)", "nav_per_aktie", "kr", False),
    ("P/NAV", "p_nav", "kvot", True),
    ("Direktavkastning", "direktavkastning_pct", "procent", True),
]
FINANSIERING = [
    ("Belåningsgrad", "belaningsgrad_pct", "procent", True),
    ("Räntetäckningsgrad", "rantetackningsgrad", "ggr", True),
    ("Snittränta på lånen", "snittranta_pct", "procent", True),
]
FASTIGHETER = [
    ("Fastighetsvärde", "fastighetsvarde_mdkr", "mdkr", True),
    ("Uthyrningsgrad", "uthyrningsgrad_pct", "procent", True),
    ("Förv.resultat/aktie (kr)", "forvaltningsresultat_per_aktie", "kr", False),
]

k1, k2, k3 = st.columns(3)
with k1:
    stil.nyckeltalspanel("Värdering", VARDERING, valt, snitt)
with k2:
    stil.nyckeltalspanel("Finansiering", FINANSIERING, valt, snitt)
with k3:
    stil.nyckeltalspanel("Fastigheter", FASTIGHETER, valt, snitt)

# --- Kursgraf (platshållare) -------------------------------------------------------
stil.platshallare(
    f"Kursgraf · {valt['ticker']}",
    "Här kommer kursen över tid att visas när riktig kursdata är inkopplad.",
    hojd=300,
)

# --- Prediktioner om bolaget -------------------------------------------------------
prediktioner = datakalla.hamta_prediktioner()
egna = prediktioner[prediktioner["bolag"] == valt["bolag"]]  # bara det valda bolaget

stil.rubrik("Prediktioner om bolaget", f"{len(egna)} st")
if egna.empty:
    stil.fotnot("Inga prediktioner om det här bolaget ännu.")
else:
    stil.tabell(egna, [
        ("datum", "Datum", "datum"),
        ("forutsagelse", "Förutsägelse", "lang"),
        ("utfall", "Utfall", "utfall"),
        ("betyg", "Betyg", "betyg"),
    ])
