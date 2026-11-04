# Snabbmatte – Matte 2

En mobilvänlig webbapp för att träna snabb huvudräkning i Matte 2, kapitlet *Algebra och icke-linjära modeller*.

- Hela appen ligger i `index.html` (HTML, CSS och JavaScript, ingen byggprocess).
- Testerna finns i `tests.html`. Öppna den via en webbserver, till exempel GitHub Pages: `…/tests.html`.
- Framsteg sparas i webbläsarens localStorage. Med konto sparas de också i molnet via Supabase, se `KONTO.md`.
- **Kapitel 2 i boken** följer bokens innehållsförteckning, 2.1–2.5 plus Sammanfattning, Testa dig själv och Blandade övningar. Avsnitten och vilka uppgiftstyper de använder står i `BOOK` i `index.html`.
- **Tidspress** är av som standard och slås på från startsidan eller boken. Uppgifter med `noTime`, miniräknaruppgifter och utmaningar har aldrig klocka. Slutbossen har det alltid.
- **Förklaringen** visas först när man trycker på knappen efter ett svar. Den går steg för steg och har en Förstår inte-knapp med enklare nivåer.
- **Guiden** är ett eget läge som leder eleven genom kapitel 2 och bedömer ärligt vilket betyg svaren visar.
  - `LADDER` i `index.html` anger för varje avsnitt vilka uppgifter som är E-, C- och A-nivå, vilka förståelsefrågor (U) som hör dit och vilka A+-utmaningar (X).
  - Varje svar loggas i `S.guide.log`, även från andra lägen. Ett svar räknas inte om eleven använt ledtråd.
  - En nivå *sitter* efter minst tre rätt i rad. Nya svar väger mest, och svaren bleknar med en halveringstid på 45 dygn.
  - C-nivå kräver även förståelsefrågor.
  - Betyget följer skolans princip: E, D, C, B eller A beroende på nivån i alla 18 avsnitt. B och A kräver dessutom Slutprovet.
  - Planeraren (`guidePlan`) gör pass om tolv uppgifter: fokus, reparation av fel, underhåll och en toppuppgift.
  - `guideAdapt` ändrar passet medan det pågår: ny chans efter fel, högre nivå efter tre rätt i rad och lägre nivå efter två fel i rad.
  - Proven är Kapitelprov (8 uppgifter), Slutprovet (12 uppgifter, låst tills alla kapitelprov är klara) och Mästarprovet (10 A+-frågor).
  - Rättningen i guiden är stenhård. Det finns inga ledtrådar, och ett avrundat svar måste ha just så många decimaler som uppgiften ber om.
