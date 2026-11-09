"""
Sida 1: Översikt
Två rutor högst upp (fastighetsindex och 10-årsränta) och en tabell
med alla bolag i bevakningslistan.
"""
import streamlit as st

import datakalla
import stil

stil.sidhuvud("BEV", "Översikt", "Svenska noterade fastighetsbolag")

# Hämta datan (just nu påhittade exempel från CSV-filerna i data/).
marknad = datakalla.hamta_marknad()
bolag = datakalla.hamta_bevakningslista()

# --- Två rutor högst upp ----------------------------------------------------
vanster, hoger = st.columns(2)
with vanster:
    stil.ruta(marknad.loc["fastighetsindex"])
with hoger:
    stil.ruta(marknad.loc["ranta_10ar"])

# --- Sortering ----------------------------------------------------------------
# Varje val i listan pekar på (kolumn att sortera efter, stigande ordning?).
SORTERING = {
    "Bolag (A–Ö)": ("bolag", True),
    "Förändring % (störst först)": ("forandring_pct", False),
    "P/NAV (lägst först)": ("p_nav", True),
    "Belåningsgrad (lägst först)": ("belaningsgrad_pct", True),
    "Räntetäckningsgrad (högst först)": ("rantetackningsgrad", False),
}
valruta, _ = st.columns([1, 3])
with valruta:
    val = st.selectbox("Sortera efter", list(SORTERING))
kolumn, stigande = SORTERING[val]
bolag = bolag.sort_values(kolumn, ascending=stigande)

# --- Tabellen -------------------------------------------------------------------
# (kolumn i datan, rubrik i tabellen, format – formaten finns i stil.py)
KOLUMNER = [
    ("bolag", "Bolag", "text"),
    ("kurs", "Kurs", "kr"),
    ("forandring_pct", "Förändring %", "forandring"),
    ("nav_per_aktie", "NAV/aktie", "kr"),
    ("p_nav", "P/NAV", "kvot"),
    ("belaningsgrad_pct", "Belåningsgrad", "procent"),
    ("rantetackningsgrad", "Räntetäckningsgrad", "ggr"),
]

# Sista raden i tabellen: snittet för hela listan. mean() är pandas
# funktion för medelvärde; numeric_only=True hoppar över textkolumnerna.
snitt = bolag.mean(numeric_only=True)
fotrad = {
    "bolag": "Snitt",
    "forandring_pct": snitt["forandring_pct"],
    "p_nav": snitt["p_nav"],
    "belaningsgrad_pct": snitt["belaningsgrad_pct"],
    "rantetackningsgrad": snitt["rantetackningsgrad"],
}

stil.rubrik("Bevakningslista", f"{len(bolag)} bolag · kurs och NAV i kronor")
stil.tabell(bolag, KOLUMNER, fotrad)
stil.fotnot(
    "P/NAV = kurs ÷ NAV per aktie (under 1,00 betyder att aktien kostar mindre än "
    "substansvärdet). Belåningsgrad = lån ÷ fastigheternas värde. Räntetäckningsgrad = "
    "hur många gånger resultatet räcker till räntorna. Mer under Begrepp i menyn."
)
