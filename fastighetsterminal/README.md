# Fastighetsterminal

En enkel terminal i Bloomberg-stil för att följa svenska noterade fastighetsbolag.
Byggd med Python, Streamlit och pandas.

> **Obs!** All data är påhittade exempelsiffror. Bolagen finns inte på riktigt.

## Starta appen

Du behöver Python 3.10 eller senare. Öppna en terminal och gå till den här mappen:

```bash
cd fastighetsterminal
```

Installera paketen (behövs bara första gången):

```bash
python -m pip install -r requirements.txt
```

Starta appen:

```bash
python -m streamlit run app.py
```

Appen öppnas i webbläsaren på <http://localhost:8501>. Stäng den med `Ctrl+C` i terminalen.
På Windows kan du behöva skriva `py` i stället för `python`.

## Så hänger filerna ihop

```
fastighetsterminal/
├── app.py               Startfilen: menyn i sidofältet och tickerremsan
├── stil.py              Utseendet: färger, typsnitt, tabeller och rutor
├── datakalla.py         Läser in datan (byt här till riktig data senare)
├── sidor/               En fil per sida i menyn
│   ├── oversikt.py
│   ├── bolag.py
│   ├── rantor.py
│   ├── prediktionslogg.py
│   └── begrepp.py
├── data/                Påhittad exempeldata
│   ├── exempel.csv              Bevakningslistan
│   ├── exempel_marknad.csv      Fastighetsindex och räntor
│   └── exempel_prediktioner.csv Prediktionsloggen
├── .streamlit/config.toml       Mörkt tema och typsnitt
└── requirements.txt     Paketen appen behöver
```

## Ändra datan

- **Lägg till ett bolag:** lägg till en rad i `data/exempel.csv`. P/NAV och
  direktavkastning räknas ut automatiskt i `datakalla.py`.
- **Ny prediktion:** lägg till en rad i `data/exempel_prediktioner.csv`. Lämna
  `utfall` och `betyg` tomma tills du vet hur det gick.
- **Riktig data:** ändra funktionerna i `datakalla.py`. Om de returnerar
  tabeller med samma kolumner behöver resten av appen inte ändras.

CSV-filerna använder kommatecken mellan kolumnerna och punkt som decimaltecken.
Om Excel visar allt i en enda kolumn, öppna filen i VS Code eller Google Kalkylark i stället.
