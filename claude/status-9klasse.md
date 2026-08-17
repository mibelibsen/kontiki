# Status · 9. klasse-sitet

Sidst opdateret: 2026-08-17

Denne fil er arbejdsloggen for sitet. Læs den først i en ny session, og opdatér
den til sidst, så næste session kan fortsætte uden at gætte.

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
| `manipulation.html` | Interaktiv side, 3 moduler + blandet quiz | Klar, **men se afhængigheder** |
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

De fleste sider har **al CSS inline** i et `<style>`-blok og al JS inline i et
`<script>`-blok, så hver fil virker alene. Fælles designtokens (`--accent:#1f6fd6`
m.fl.) er kopieret ind i hver fil.

De interaktive sider gemmer elevens navn og svar i `localStorage` via en
`data-store-key` på `<body>` (fx `man9_state_v1`), så ungen kan fortsætte hvor
hen slap.

## Åbne punkter

1. **`manipulation.html` bruger eksterne filer.** Den er den eneste side uden
   inline CSS/JS — den henter `/style.css` og `/app.js` fra sitets rod. De to
   filer er ikke i repoet. Enten mangler de i uploadet, eller også er siden
   ustylet når den åbnes lokalt. **Skal afklares:** findes de på det deployede
   site, eller skal CSS/JS inlines som på de andre sider?
2. **Facit-filerne er ikke linket** fra nogen side. Tre facit-ressourcer ligger
   i repoet uden indgang. Bevidst (så unger ikke finder dem) eller glemt?
3. **`model-fra-anden-chat/`** er en næsten identisk kopi af `manipulation.html`
   med absolutte links (`/statistik.html`) plus tre manipulation-PDF'er der
   ikke findes i roden. Enten flyt PDF'erne op og slet mappen, eller behold den
   som arkiv.
4. **Manipulation mangler et hjemmeopgave-ark** — statistik har ét, det har
   funktioner og manipulation ikke.
5. **Ingen "tilbage til forsiden"** fra `statistik.html` og `manipulation.html`
   — de linker kun til `matematik.html`.
6. **Årsplaner til samfundsfag og tysk** mangler stadig.

## Næste skridt

Ikke besluttet. Afklar punkt 1 først — det er det eneste der kan gøre en side
ubrugelig for eleverne.
