"""
Fastighetsterminal – startfilen.

Starta appen med:   python -m streamlit run app.py

Filen gör tre saker:
1. Ställer in sidan (titel, bred layout) och laddar terminalutseendet.
2. Visar den rullande tickerremsan högst upp (den syns på alla sidor).
3. Bygger menyn i sidofältet och visar sidan man har valt.

Själva sidorna ligger i mappen sidor/, en fil per sida.
"""
import streamlit as st

import datakalla
import stil

st.set_page_config(
    page_title="Fastighetsterminal",
    page_icon=":material/apartment:",
    layout="wide",  # använd hela skärmbredden
)
stil.ladda_stil()

# Menyn: en rad per sida (fil, namn i menyn, ikon).
# Vill du lägga till en sida skapar du en ny fil i sidor/ och en ny rad här.
sidor = [
    st.Page("sidor/oversikt.py", title="Översikt", icon=":material/table_rows:", default=True),
    st.Page("sidor/bolag.py", title="Bolag", icon=":material/apartment:"),
    st.Page("sidor/rantor.py", title="Räntor", icon=":material/percent:"),
    st.Page("sidor/prediktionslogg.py", title="Prediktionslogg", icon=":material/edit_note:"),
    st.Page("sidor/begrepp.py", title="Begrepp", icon=":material/menu_book:"),
]
vald_sida = st.navigation(sidor)

stil.sidofalt_info()
stil.tickerremsa(datakalla.hamta_bevakningslista())

# Kör filen för den sida som är vald i menyn.
vald_sida.run()
