# Opsætning af mibelibsen.space — én gang, så det bare kører

Sidst opdateret: 2026-08-17

## Hvorfor det er gået galt hele dagen

Sitet er indtil nu blevet deployet af Claude **gennem** Vercel. Den vej virker
ikke: adgangen til Vercel i chatten kan oprette ting, men hverken læse dem igen
eller udgive dem. Hvert forsøg lykkes derfor halvt, og næste forsøg starter
oven på noget halvfærdigt. Det er dét mønster, der har gentaget sig.

## Løsningen

Vi fjerner Claude fra deploy-leddet.

```
Claude  →  GitHub (mibelibsen/kontiki, branch main)  →  Vercel  →  mibelibsen.space
```

Vercel kobles til GitHub **én gang**. Derefter holder Vercel selv øje med
repoet: hver gang der kommer noget nyt på `main`, lægger den det op af sig selv,
typisk på under et minut. Claudes Vercel-adgang skal aldrig bruges igen.

## Trin for trin

Rækkefølgen er vigtig. Sitet er oppe hele vejen igennem, og du sletter først
det gamle, når det nye beviseligt virker.

### 1. Find ud af hvor domænet ligger nu

👉 **https://vercel.com/mibelibsens-projects/~/domains**

Find `mibelibsen.space` på listen. Kolonnen ved siden af viser, hvilket projekt
det peger på. **Skriv projektnavnet ned** — du skal bruge det i trin 6 og 7.

Står domænet der slet ikke, ligger det i en anden Vercel-konto end teamet
`mibelibsens-projects`. Sig til, hvis det er tilfældet.

### 2. Se hvad der allerede findes

👉 **https://vercel.com/mibelibsens-projects**

Her er alle projekter. Du leder efter to navne:

- **`kontiki-9klasse`** — oprettede jeg under fejlsøgningen. Det er allerede
  koblet til det rigtige GitHub-repo, men har aldrig udgivet noget. Findes det,
  så brug det i trin 3 og spring importen over.
- **`kontiki`** — findes et sted i kontoen, men jeg kan ikke se det. Er det på
  listen, så åbn det og se under Settings → Git, om det peger på
  `mibelibsen/kontiki`.

### 3. Sørg for at der er et projekt koblet til repoet

**Findes `kontiki-9klasse`:** åbn projektets Git-indstillinger.

👉 **https://vercel.com/mibelibsens-projects/kontiki-9klasse/settings/git**

Tjek at Repository står til `mibelibsen/kontiki`, og sæt **Production Branch**
til `main`. Gem.

**Findes det ikke:** importér repoet på ny.

👉 **https://vercel.com/new/mibelibsens-projects**

Vælg `mibelibsen/kontiki` på listen og tryk *Import*. Under *Framework Preset*
vælger du **Other**. Build Command og Output Directory skal stå tomme — det er
rene HTML-filer, der bare skal serveres. Tryk *Deploy*.

### 4. Sæt gang i den første udgivelse

👉 **https://vercel.com/mibelibsens-projects/kontiki-9klasse/deployments**

Er listen tom, så tryk på knappen *Redeploy* øverst, eller *Create Deployment*
og vælg branchen `main`.

Vent til den øverste linje står som **Ready**.

### 5. Tjek at sitet virker, før du rører domænet

Klik på den øverste deployment i listen. Vercel viser en adresse i stil med
`kontiki-9klasse-xxxx.vercel.app`. Åbn den.

Tjek tre ting:

- Forsiden har farver og de fire fagkort.
- Matematiksiden viser seks kort, heriblandt *Hjemmeopgaver: Manipulation*.
- Manipulation-siden spørger om dit fornavn, og quizzen svarer rigtigt/forkert
  når du klikker.

**Gå først videre, når alle tre virker.** Gør de ikke det, så stop her og sig
til — så retter jeg det, før domænet flyttes.

### 6. Flyt domænet til det nye projekt

Først væk fra det gamle. Sæt det projektnavn ind, du skrev ned i trin 1:

👉 `https://vercel.com/mibelibsens-projects/`**`DET-GAMLE-PROJEKT`**`/settings/domains`

Fjern `mibelibsen.space` og `www.mibelibsen.space` dér.

Så over på det nye:

👉 **https://vercel.com/mibelibsens-projects/kontiki-9klasse/settings/domains**

Tilføj begge: `mibelibsen.space` og `www.mibelibsen.space`.

Åbn https://www.mibelibsen.space og hold `Shift` nede mens du genindlæser.

### 7. Ryd op i Vercel

Slet det gamle projekt. Knappen sidder nederst på siden under *Delete Project*:

👉 `https://vercel.com/mibelibsens-projects/`**`DET-GAMLE-PROJEKT`**`/settings`

Fandt du også et projekt ved navn `kontiki` i trin 2, og var det ikke det
samme, så slet det ligeledes:

👉 **https://vercel.com/mibelibsens-projects/kontiki/settings**

### 8. Ryd op på GitHub

Sæt default-branch til `main`. Feltet hedder *Default branch* og sidder et
stykke nede på siden:

👉 **https://github.com/mibelibsen/kontiki/settings**

Slet derefter den gamle arbejdsbranch — tryk på skraldespanden ud for
`claude/status-9klasse-op6yol`:

👉 **https://github.com/mibelibsen/kontiki/branches**

## Bagefter

Reglen er enkel: **det, der ligger på `main`, er det, der ligger på sitet.**

Når du beder om en ændring, pusher jeg til `main`, og Vercel lægger den op selv.

Går noget galt, kan du rulle tilbage: åbn
👉 **https://vercel.com/mibelibsens-projects/kontiki-9klasse/deployments**,
find en version der virkede, tryk på de tre prikker til højre og vælg
*Promote to Production*. Ét klik, og sitet er tilbage som før.

## Hvis noget driller

- **Ændringen kan ikke ses.** Tjek på deployments-siden, at den øverste står som
  *Ready* og *Production*. Ellers hold `Shift` og genindlæs siden.
- **Siden er uden farver og layout.** Så mangler en fil. Alle sider er
  selvbærende nu, så det bør ikke kunne ske — det var netop manipulation-sidens
  fejl.
- **Vercel bygger ikke ved et push.** Tjek Production Branch på
  👉 **https://vercel.com/mibelibsens-projects/kontiki-9klasse/settings/git**
