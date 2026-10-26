# Konton och molnsparning

Appen kan spara framstegen i molnet med [Supabase](https://supabase.com), som har en gratisnivå. Så länge `CLOUD` i `index.html` är tom är kontodelen avstängd, och allt sparas bara lokalt i webbläsaren.

## Så fungerar det

- **Registrering:** spelaren väljer användarnamn, e-post och lösenord. En sifferkod skickas till e-postadressen, och kontot är klart när koden har skrivits in.
- **Inloggning:** e-post och lösenord. Har man glömt lösenordet får man en kod på mejlen och väljer ett nytt.
- **Molnsparning:** framstegen sparas i molnet ett par sekunder efter varje sparning, och när appen stängs eller hamnar i bakgrunden. Saknas internet sparas de när anslutningen kommer tillbaka.
- **Flera enheter:** vid start och inloggning hämtas de senaste framstegen. Har både enheten och kontot egna framsteg får spelaren välja vilka som ska gälla.
- **Utan konto:** "Fortsätt utan konto" fungerar precis som tidigare.

## Sätta upp Supabase (cirka 15 minuter)

1. **Skapa ett projekt.** Skapa ett konto på supabase.com och ett nytt projekt. Välj en region i Europa, till exempel Stockholm.
2. **Skapa tabellerna.** Gå till **SQL Editor → New query**, klistra in hela [`supabase/setup.sql`](supabase/setup.sql) och tryck **Run**.
3. **Slå på e-postverifiering.** Kontrollera under **Authentication → Sign In / Providers → Email** att Email är på och att **Confirm email** är påslaget.
4. **Skicka kod i stället för länk.** Gå till **Authentication → Emails → Templates**.
   - I mallen **Confirm signup** byter du ut länken mot koden. Exempel:
     ```html
     <h2>Välkommen till Snabbmatte!</h2>
     <p>Din kod är:</p>
     <h1>{{ .Token }}</h1>
     ```
   - Gör likadant i mallen **Reset password**, med texten "Din kod för nytt lösenord är:".
5. **Koppla in en egen e-posttjänst (SMTP).** Supabases inbyggda e-post skickar bara till adresser i ditt eget Supabase-team och bara ett par mejl i timmen. Därför behövs en egen tjänst för riktiga användare. Fyll i den under **Authentication → Emails → SMTP Settings**.
   - **Enklast är Gmail.** Slå på tvåstegsverifiering för ditt Google-konto, skapa ett *applösenord* och fyll sedan i:
     - värd `smtp.gmail.com`
     - port `465`
     - användarnamn: din Gmail-adress
     - lösenord: applösenordet
   - Gmail räcker till cirka 500 mejl per dag. Med en egen domän kan du i stället använda Resend eller Brevo.
6. **Ange appens adress.** Sätt **Site URL** till `https://felixwiklund000.github.io/matteapp/` under **Authentication → URL Configuration**.
7. **Hämta adress och nyckel.** Under **Project Settings → API** kopierar du **Project URL** och den publika nyckeln (**anon** eller **publishable**). Använd aldrig nyckeln som heter `service_role` eller `secret`.
8. **Lägg in dem i appen.** Fyll i dem längst ned i `index.html`:
   ```js
   const CLOUD={url:'https://xxxx.supabase.co', anonKey:'din-publika-nyckel'};
   ```
   Pusha sedan till `main`.

Den publika nyckeln får ligga i koden. Databasreglerna i `setup.sql` (Row Level Security) gör att varje konto bara kan läsa och ändra sina egna framsteg.
