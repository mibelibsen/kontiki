# Status · 9. klasse-sitet

Sidst opdateret: 2026-08-17

Denne fil er arbejdsloggen for sitet. Læs den først i en ny session, og opdatér
den til sidst, så næste session kan fortsætte uden at gætte.

**Deploy virker ikke — læs `claude/deploy.md` før du forsøger.** Kort: domænet
mibelibsen.space sidder på et Vercel-projekt som denne sessions forbindelse
hverken kan se eller deploye til. Det kræver en rettelse i Vercel-kontoen, ikke
i koden.

> **Bemærk:** Denne fil fandtes ikke i repoet, da den blev efterspurgt første
> gang (repoet var tomt, og zip-filen indeholdt kun HTML/PDF/XLSX). Indholdet
> nedenfor er rekonstrueret ud fra de faktiske filer i uploadet — ikke fra en
> tidligere status-fil. Hvis der findes en original, så indsæt den i stedet.

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
| `model-fra-anden-chat/` | Ældre variant af manipulation + 3 PDF'er | Duplikat, bør ryddes op |

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

1. **Facit-filerne er ikke linket** fra nogen side. Tre facit-ressourcer ligger
   i repoet uden indgang. Bevidst (så unger ikke finder dem) eller glemt?
2. **`model-fra-anden-chat/`** er en næsten identisk kopi af `manipulation.html`
   med absolutte links (`/statistik.html`) plus tre manipulation-PDF'er der
   ikke findes i roden. Enten flyt PDF'erne op og slet mappen, eller behold den
   som arkiv. Bemærk at kopien stadig peger på `/style.css` og `/app.js`.
3. **Manipulation mangler et hjemmeopgave-ark** — statistik har ét, det har
   funktioner og manipulation ikke.
4. **`statistik.html` mangler stadig "tilbage til forsiden"** — den linker kun
   til `matematik.html`. Manipulation har fået linket.
5. **Årsplaner til samfundsfag og tysk** mangler stadig.
6. **`/style.css` og `/app.js` på det deployede site** bruges nu ikke længere af
   nogen side i repoet. Tjek om de kan fjernes fra deployet.

## Næste skridt

Ikke besluttet — tag et af punkterne ovenfor.
