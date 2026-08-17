# Status · 9. klasse-sitet

Sidst opdateret: 2026-08-17

Denne fil er arbejdsloggen for sitet. Læs den først i en ny session, og opdatér
den til sidst, så næste session kan fortsætte uden at gætte.

**Deploy:** Vercel-projektet `kontiki-9klasse` er koblet til dette repo og
bygger ved hvert push til `main`. Mangler kun at få domænet flyttet over fra
`kontiki9`. Se `claude/opsaetning.md`. Claudes egen Vercel-adgang kan ikke
bruges og skal ikke bruges — Git-koblingen klarer det.

> **Bemærk:** Denne fil fandtes ikke i repoet, da den blev efterspurgt første
> gang (repoet var tomt, og zip-filen indeholdt kun HTML/PDF/XLSX). Indholdet
> er rekonstrueret ud fra de faktiske filer i uploadet — ikke fra en tidligere
> status-fil.

## Hvad sitet er

Statisk undervisningssite til 9. klasse. Ingen build, ingen dependencies —
rene HTML-filer der åbnes direkte eller serveres fra roden.
Sproget er dansk hele vejen igennem. Eleverne omtales "unger".

## Filoversigt

| Fil | Rolle | Status |
|---|---|---|
| `index.html` | Forside, fagoversigt | Klar |
| `matematik.html` | Fagforside for matematik, kort til undersider | Klar |
| `samfundsfag.html` | Fagside | **Placeholder** — "Afventer indhold" |
| `tysk.html` | Fagside | **Placeholder** — "Afventer indhold" |
| `aarsplan-matematik.html` | Årsplan 2026/27, uge 33 → uge 6 + repetition | Klar, linker til xlsx |
| `aarsplan-matematik-2026-27.xlsx` | Download-version af årsplanen | Klar |
| `statistik.html` | Interaktiv side, 4 moduler + blandet quiz | Klar |
| `funktioner-og-ligninger.html` | Interaktiv side, 26 quizspørgsmål | Klar |
| `manipulation.html` | Interaktiv side, 3 moduler + blandet quiz | Klar, selvbærende
| `statistik-hjemmeopgaver.html` | 35 opgaver til print/aflevering | Klar |
| `facitark-funktioner-og-ligninger.html` | Facit som HTML | Klar, **ikke linket fra nogen side** |
| `facit-statistik-online.pdf` | Facit til statistik-siden | **Ikke linket** |
| `facit-statistik-hjemmeopgaver.pdf` | Facit til hjemmeopgaverne | **Ikke linket** |
| `lektier-manipulation.pdf` | Opgaveark til manipulation | Linket fra `matematik.html` |
| `facitark-manipulation.pdf` | Facit til manipulation-siden | **Ikke linket** |
| `facit-lektier-manipulation.pdf` | Facit til opgavearket | **Ikke linket** |

## Fagfaner

- **Matematik** — indhold på plads (3 interaktive sider, 1 opgaveark, årsplan).
- **Samfundsfag** — tom fane, venter på en årsplan (fx et regneark som til matematik).
- **Tysk** — tom fane, venter på en årsplan.
- **Fysik** — vist som "Kommer snart" i navigationen, ingen side endnu.

## Teknisk mønster

**Alle** sider har nu al CSS inline i et `<style>`-blok og al JS inline i et
`<script>`-blok, så hver fil virker alene. Fælles designtokens (`--accent:#1f6fd6`
m.fl.) er kopieret ind i hver fil.

De interaktive sider gemmer elevens navn og svar i `localStorage`. Quiz-motoren i
`manipulation.html` er den generelle udgave: den læser `data-store-key` (nøglen i
localStorage) og `data-modules` (modulnavne til resultattabellen, adskilt af `|`)
fra `<body>`, så den kan genbruges på en ny emneside uden at blive rettet.
`statistik.html` og `funktioner-og-ligninger.html` har stadig hver deres kopi med
hårdkodede værdier.

Quiz-markuppen er ens på tværs af siderne: `.quiz` > `.q[data-answer][data-exp]`
> `.opt`, plus `.fb` til feedback og et `[data-score]`-badge pr. quiz. Siden skal
have disse id'er: `startOverlay`, `nameInput`, `ovTitle`, `ovText`, `startBtn`,
`skipBtn`, `resetBtn`, `switchBtn`, `welcomeBar`, `welcomeHi`, `welcomeLive`,
`progressFill`, `progressLabel`, `resultsBody`, `gradeMsg`, `finalMsg`.

## Åbne punkter

1. **Fire facit-filer er ikke linket** fra nogen side. Bevidst (så unger ikke
   finder dem) eller glemt?
2. **Funktioner og ligninger mangler et opgaveark.** Statistik og manipulation
   har hver ét; funktioner har kun et facitark.
3. **`statistik.html` mangler "tilbage til forsiden"** — den linker kun til
   `matematik.html`. Manipulation har fået linket.
4. **Årsplaner til samfundsfag og tysk** mangler stadig.
5. **Quiz-motoren findes i tre kopier.** Kun `manipulation.html` har den
   generelle udgave. `statistik.html` og `funktioner-og-ligninger.html` har
   hver deres med hårdkodet nøgle og modulnavne. Kan samles, hvis en side mere
   skal laves.

## Næste opgave — indhold

Aftalt 17. august 2026: **først deploy-flowet, derefter indholdet.**

Sitet er set live på `kontiki-9klasse.vercel.app` og indeholder fejl. Brugeren
nævner to ting, som skal tages fat på, når deploy virker:

1. **Matematikken skal gennemgås.** Regnestykker, facit og forklaringer på de
   interaktive sider er ikke verificeret. Der er ikke lavet et gennemløb af,
   om `data-answer` peger på det rigtige svar, eller om udregningerne holder.
2. **Manglende opgaver.** Hvilke der mangler, er endnu ikke specificeret.

Derudover: brugeren nævner rettelser fra andre chats, som er "kommet med" i
den udgave der ligger live. Afklar hvilke, før noget skrives om — der kan ligge
arbejde i den live-udgave, som ikke findes i dette repo.

Bed om en konkret liste over fejl frem for at gætte. Når deploy-flowet virker,
kan hver rettelse ses live under et minut efter et push.

## Løst undervejs

- `manipulation.html` hentede `/style.css` og `/app.js` fra sitets rod og lå
  ustylet. Begge dele er nu inline, og motoren er gjort generel.
- Dubletmappen `model-fra-anden-chat/` er slettet. Dens tre PDF'er var unikke
  og ligger nu i roden.
- `lektier-manipulation.pdf` var ikke linket nogen steder og har fået et kort
  på `matematik.html`.
