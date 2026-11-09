"""
Sida 3: Räntor
Styrräntan och 10-årsräntan, med platshållare för graferna och en kort
förklaring av varför räntan är så viktig för fastighetsbolag.
"""
import streamlit as st

import datakalla
import stil

stil.sidhuvud("RNT", "Räntor", "Styrränta och svensk 10-årsränta")

marknad = datakalla.hamta_marknad()

vanster, hoger = st.columns(2)
with vanster:
    stil.ruta(marknad.loc["styrranta"])
    stil.platshallare(
        "Styrränta · historik",
        "Här kommer Riksbankens styrränta över tid att visas.",
    )
with hoger:
    stil.ruta(marknad.loc["ranta_10ar"])
    stil.platshallare(
        "10-årsränta · historik",
        "Här kommer räntan på svenska tioåriga statsobligationer att visas.",
    )

stil.rubrik("Därför spelar räntan roll för fastighetsbolag")
stil.textruta("""
<ol>
  <li><b>Räntekostnader.</b> Fastighetsbolag lånar mycket. Stiger räntan blir lånen dyrare,
      och då sjunker förvaltningsresultatet och räntetäckningsgraden.</li>
  <li><b>Fastigheternas värde.</b> När räntan stiger vill köpare ha högre avkastning på
      fastigheter. Då sjunker värdet, och med det NAV, medan belåningsgraden stiger.</li>
  <li><b>Aktiekursen.</b> Börsen tittar framåt. Fastighetsaktier rör sig ofta när
      10-årsräntan rör sig, långt innan det syns i bolagens rapporter.</li>
</ol>
<p class="dov" style="margin:8px 0 0">Styrräntan påverkar främst korta lån med rörlig ränta.
10-årsräntan visar vad marknaden tror om räntorna på lång sikt.</p>
""")
