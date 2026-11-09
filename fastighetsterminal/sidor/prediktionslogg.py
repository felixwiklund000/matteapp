"""
Sida 4: Prediktionslogg
Här skriver du ner vad du tror ska hända, och varför. När facit finns
fyller du i utfallet och sätter ett betyg 1–5 på din förutsägelse.
"""
import streamlit as st

import datakalla
import stil

stil.sidhuvud("PRED", "Prediktionslogg", "Mina förutsägelser och hur de gick")

prediktioner = datakalla.hamta_prediktioner()

# --- Fyra små siffertavlor ------------------------------------------------------
# notna() är True för rader som HAR ett betyg, alltså de som är bedömda.
bedomda = prediktioner[prediktioner["betyg"].notna()]
snittbetyg = bedomda["betyg"].mean()

k1, k2, k3, k4 = st.columns(4)
with k1:
    stil.siffra("Prediktioner", len(prediktioner))
with k2:
    stil.siffra("Bedömda", len(bedomda))
with k3:
    stil.siffra("Väntar på utfall", len(prediktioner) - len(bedomda))
with k4:
    stil.siffra("Snittbetyg", f"{stil.tal(snittbetyg, 1)} / 5")

# --- Tabellen -------------------------------------------------------------------------
KOLUMNER = [
    ("datum", "Datum", "datum"),
    ("bolag", "Bolag", "text"),
    ("forutsagelse", "Förutsägelse", "lang"),
    ("motivering", "Motivering", "lang"),
    ("utfall", "Utfall", "utfall"),
    ("betyg", "Betyg (1–5)", "betyg"),
]
stil.rubrik("Logg", "nyast först")
stil.tabell(prediktioner, KOLUMNER)
stil.fotnot(
    "Så använder du loggen: skriv förutsägelsen och motiveringen INNAN du vet svaret. "
    "Fyll i utfall och betyg när facit finns (5 = helt rätt, 1 = helt fel). "
    "Just nu ändrar du i filen data/exempel_prediktioner.csv."
)
