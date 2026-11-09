"""
Datakällan – det ENDA stället i appen som vet var datan kommer ifrån.

Just nu läser vi påhittade exempelsiffror från CSV-filerna i mappen data/.
När du vill använda riktig data byter du bara ut innehållet i funktionerna
här. Resten av appen behöver inte ändras, så länge funktionerna fortfarande
returnerar tabeller (pandas DataFrames) med samma kolumner.
"""
from pathlib import Path

import pandas as pd

# Mappen där CSV-filerna ligger. Vi räknar ut den utifrån var den här filen
# ligger, så att appen hittar datan oavsett varifrån du startar den.
DATAMAPP = Path(__file__).parent / "data"


def hamta_bevakningslista() -> pd.DataFrame:
    """Bevakningslistan: ett bolag per rad (från data/exempel.csv)."""
    df = pd.read_csv(DATAMAPP / "exempel.csv")

    # Två nyckeltal räknar vi ut själva i stället för att skriva in dem:
    # P/NAV = aktiekurs delat med substansvärde (NAV) per aktie.
    df["p_nav"] = df["kurs"] / df["nav_per_aktie"]
    # Direktavkastning (för aktien) = utdelning delat med kurs, i procent.
    df["direktavkastning_pct"] = df["utdelning_per_aktie"] / df["kurs"] * 100

    return df


def hamta_marknad() -> pd.DataFrame:
    """Index och räntor, en rad per serie (från data/exempel_marknad.csv).

    Kolumnen 'id' blir radnamn, så att man kan skriva
    marknad.loc["ranta_10ar"] för att få fram 10-årsräntan.
    """
    return pd.read_csv(DATAMAPP / "exempel_marknad.csv", index_col="id")


def hamta_prediktioner() -> pd.DataFrame:
    """Prediktionsloggen, nyast först (från data/exempel_prediktioner.csv)."""
    df = pd.read_csv(DATAMAPP / "exempel_prediktioner.csv", parse_dates=["datum"])
    return df.sort_values("datum", ascending=False)
