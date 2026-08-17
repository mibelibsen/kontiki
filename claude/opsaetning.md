# Opsætning af mibelibsen.space

Sidst opdateret: 2026-08-17

## Om links i denne fil

Claude kan **ikke** tilgå vercel.com fra sit arbejdsmiljø — netværket blokerer
det, og Vercels dokumentation indeholder kun CLI- og API-kommandoer, ingen
dashboard-adresser. Adresser til Vercel-dashboardet kan derfor ikke verificeres
herfra.

Derfor er hvert link nedenfor mærket:

- ✅ **Bekræftet** — verificeret i praksis.
- 🔎 **Ubekræftet** — sandsynligt mønster, men gættet. Virker det ikke, så brug
  klikvejen der står lige under.
- 🖱️ **Klikvej** — ingen adresse, kun præcis hvilket element der skal klikkes.

Skriv aldrig et ubekræftet link uden mærket. Det er bedre at beskrive et klik
end at gætte en adresse.

## Hvorfor det gik galt

Sitet blev deployet af Claude **gennem** Vercel. Den vej virker ikke: adgangen
kan oprette ting, men hverken læse dem igen eller udgive dem. Hvert forsøg
lykkes halvt, og det næste bygger oven på noget halvfærdigt.

## Løsningen

Claude fjernes fra deploy-leddet.

```
Claude  →  GitHub (mibelibsen/kontiki, main)  →  Vercel  →  mibelibsen.space
```

Vercel kobles til GitHub én gang. Derefter udgiver Vercel selv ved hvert push.
Claudes Vercel-adgang bruges aldrig igen.

## Projekterne på Vercel

Bekræftet 17. august 2026 ud fra Vercel-dashboardet. Der blev oprettet omkring
ti projekter til dette ene site i løbet af dagen. **Kun ét har en Git-kobling.**
Resten står med "Connect Git Repository" — tomme skaller uden kilde, som hverken
kan bygge noget eller gå i stykker.

**Behold:**

| Projekt | Hvorfor |
|---|---|
| `kontiki-9klasse` | Eneste med Git-kobling til `mibelibsen/kontiki`. Bygger ved push. Det er sitet. |

**Slet** — i denne rækkefølge:

1. `kontiki9` — har domænet i dag. Slettes **først når** domænet er flyttet.
2. `mibelibsen9`
3. `mibelibsen-space`
4. `kontiki` (`kontiki-beta.vercel.app`)
5. `mibelibsen-9klasse`
6. `mibelibsen-skole`
7. `mibelibsen-site`
8. `matematik-9-kontiki-probe`
9. `funktioner-og-ligninger-kontiki`

**Rør ikke:** `store51`, `kazzen-app`, `s51pos-api`, `s51pos-mobil`,
`s51pos-demo`, `dog-lovers-app`. De hører til andre projekter.

Claudes Vercel-adgang kan kun læse fem projekter. `get_project` på `kontiki9`
svarer `404`, `list_deployments` svarer `403`. Adgangen er begrænset på
projektniveau. Det behøver ikke rettes: Git-koblingen på `kontiki-9klasse`
virker uafhængigt af den, og det er dén, der udgiver sitet.

## Trin for trin

Planen er at flytte domænet hen på det projekt, der allerede bygger koden —
ikke at koble det tomme projekt til Git. Det er færrest trin.

### 1. Se om koden er live

✅ **https://kontiki-9klasse.vercel.app**

Tjek:

- Forsiden har farver og fire fagkort.
- Matematiksiden viser seks kort, heriblandt *Hjemmeopgaver: Manipulation*.
- Manipulation-siden spørger om fornavn, og quizzen svarer rigtigt/forkert.

### 2. Flyt domænet

🖱️ **Klikvej:** **Projects** → **kontiki-9klasse** → fanen **Settings** →
**Domains** → skriv `www.mibelibsen.space` → **Add**.

Vercel svarer, at domænet bruges af `kontiki9`, og spørger om det skal flyttes.
**Sig ja.** Gentag med `mibelibsen.space`.

`kontiki9` skal ikke åbnes.

### 3. Tjek sitet

Åbn https://www.mibelibsen.space og genindlæs med `Shift` nede.

### 4. Ryd op

Slet `kontiki9`, `mibelibsen-skole` og `mibelibsen-site`. Sletteknappen ligger
nederst på projektets **Settings**-side under *Delete Project*.

✅ **https://github.com/mibelibsen/kontiki/settings** — sæt *Default branch*
til `main`.

✅ **https://github.com/mibelibsen/kontiki/branches** — slet
`claude/status-9klasse-op6yol`.

### 5. Tjek Production Branch

🖱️ **Klikvej:** **kontiki-9klasse** → **Settings** → **Git** → feltet
**Production Branch**. Skal stå til `main`.

## Bagefter

**Det, der ligger på `main`, er det, der ligger på sitet.**

Claude pusher til `main`, og Vercel udgiver selv. Går noget galt, kan enhver
tidligere version sættes tilbage:

🖱️ **Klikvej:** projektet → **Deployments** → find en version der virkede →
`...`-menuen til højre → **Promote to Production**.

## Hvis noget driller

- **Ændringen kan ikke ses.** Tjek under **Deployments**, at øverste række står
  som *Ready* og *Production*. Ellers genindlæs med `Shift` nede.
- **Siden mangler farver.** Så mangler en fil. Alle sider er selvbærende nu, så
  det bør ikke kunne ske.
- **Intet sker ved et push.** Tjek Production Branch, trin 2.
