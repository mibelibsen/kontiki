# kontiki · undervisningssite til 9. klasse

Statisk undervisningssite til matematik i 9. klasse. Live på
**https://www.mibelibsen.space**

Dette er den samlede dokumentation. Læs den før du ændrer noget.

---

## Indhold

1. [Sådan er sitet bygget](#sådan-er-sitet-bygget)
2. [Deploy](#deploy)
3. [Filoversigt](#filoversigt)
4. [De seks regler](#de-seks-regler)
5. [Lektier og facit](#lektier-og-facit)
6. [Quiz-motoren](#quiz-motoren)
7. [Figurer](#figurer)
8. [Sådan tester du](#sådan-tester-du)
9. [Planlagte opgaver](#planlagte-opgaver)
10. [Øvrig dokumentation](#øvrig-dokumentation)

---

## Sådan er sitet bygget

Rene HTML-filer. **Intet build, ingen dependencies, ingen pakkehåndtering.** Man
åbner en fil i en browser, og den virker.

Hver side er **selvbærende**: al CSS ligger i et `<style>`-blok og al JS i et
`<script>-blok` inde i filen selv. Fælles designtokens (`--accent:#1f6fd6` m.fl.)
er kopieret ind i hver fil.

> **Hent aldrig CSS eller JS fra sitets rod.** `manipulation.html` gjorde det
> engang — den hentede `/style.css` og `/app.js` — og lå ustylet med død quiz,
> fordi filerne ikke fulgte med. Det er den dyreste fejl, sitet har haft.

Sproget er dansk hele vejen igennem, også i commit-beskeder og dokumentation.
Eleverne omtales **"unger"**.

## Deploy

```
Claude → GitHub (mibelibsen/kontiki, main) → Vercel (kontiki-9klasse) → mibelibsen.space
```

**`main` er sandheden.** Det der ligger på `main`, ligger på sitet. Vercel bygger
selv ved hvert push; siden er live under et minut senere.

Vercel-projektet er `kontiki-9klasse` og har begge domæner:
https://vercel.com/mibelibsens-projects/kontiki-9klasse/settings/domains

**Brug ikke Vercels API.** Claudes Vercel-adgang er begrænset på projektniveau og
kan hverken læse projektet eller udgive — `get_project` svarer `404`,
`list_deployments` svarer `403`. Git-koblingen klarer det hele og er uafhængig
af den adgang.

Skal en ændring rulles tilbage:
https://vercel.com/mibelibsens-projects/kontiki-9klasse/deployments → find en
version der virkede → `...` → **Promote to Production**.

Detaljer i [`claude/opsaetning.md`](claude/opsaetning.md).

## Filoversigt

### Sider der udgives

| Fil | Rolle |
|---|---|
| `index.html` | Forside med fagoversigt |
| `matematik.html` | Fagforside, kort til alle matematiksider |
| `samfundsfag.html` | Fagside — **placeholder**, afventer årsplan |
| `tysk.html` | Fagside — **placeholder**, afventer årsplan |
| `aarsplan-matematik.html` | Årsplan 2026/27, uge 33 → uge 6 + repetition |
| `aarsplan-matematik-2026-27.xlsx` | Årsplanen som download |
| `statistik.html` | Interaktiv side: 4 moduler, quiz, Opgave A–D |
| `funktioner-og-ligninger.html` | Interaktiv side: quiz. **Mangler åbne opgaver** |
| `manipulation.html` | Interaktiv side: 3 moduler, quiz, Opgave A–D |
| `lektier-uge33-beskriv-data.html` | Lektier uge 33 |
| `lektier-uge34-diagrammer.html` | Lektier uge 34 |

### Mapper der IKKE udgives

Udelukket i `.vercelignore`, så de findes ikke på sitet:

| Mappe | Indhold |
|---|---|
| `facit/` | Alle facitlister. **Må aldrig udgives.** |
| `kommende/` | Lektier der endnu ikke er givet |
| `claude/` | Arbejdslog og dokumentation |

`.vercelignore` er den eneste beskyttelse af facit. **Ret den ikke** uden at
tænke over konsekvensen: en fil i roden er offentlig, også hvis intet linker til
den.

## De seks regler

1. **Svar altid på dansk** — også i commit-beskeder og dokumentation.
2. **Altid dybe links.** Skal brugeren gøre noget i en webgrænseflade, så giv et
   direkte link til præcis den side. Aldrig "gå ind under Settings → Git", altid
   `https://vercel.com/<team>/<projekt>/settings/git`. Kan adressen ikke
   verificeres, så skriv den alligevel og ret den hvis den fejler — en klikvej er
   ikke et acceptabelt alternativ.
3. **Facit kommer aldrig på sitet.** Facit ligger i `facit/` og sendes i Code.
4. **Lektier er altid åbne opgaver.** Multiple choice er aldrig lektier.
5. **Intet udgives før den dag, lektien gives.**
6. **Altid visuelle eksempler.** Hver opgave og hver forklaring skal have en
   figur — også facitlisterne. Se [Figurer](#figurer).

Reglerne står også i [`CLAUDE.md`](CLAUDE.md), som Claude læser automatisk.

## Lektier og facit

**Lektier** er åbne opgaver med bogstav og delspørgsmål a, b, c — bygget over
modulopgaverne på klassens sider, men med andre tal. Multiple choice hører kun
til som quiz på skoledelen; det er noget ungerne selv kan øve sig på, ikke noget
der stilles for.

Besvarelsesformuleringen er altid:
> *"Lav udregninger i Word med Geogebra eller Excel og vis din metode."*

**Facitlisterne** ligger i `facit/` som PDF, én pr. dag og emne, i to serier:

| Serie | Titelformat |
|---|---|
| Modulopgaver | `Facitliste Matematik <ugedag> den <dato> <emne> facitliste` |
| Lektier | `Facitliste lektier Matematik <ugedag> den <dato> <emne> facitliste` |

Datoen på en lektie-facitliste er **den dag lektien blev givet**.

Filnavne følger `facit-<serie>-<ÅÅÅÅ-MM-DD>-<emne>.pdf`, så de sorterer
kronologisk.

**Sådan udgives en lektie:**

```bash
git mv kommende/lektier-ugeNN-navn.html .
# tilføj et kort på matematik.html i samme mønster som de øvrige lektiekort
git commit && git push
```

Planen for hvilken uge der hører til hvad står i
[`claude/lektieplan.md`](claude/lektieplan.md).

## Quiz-motoren

De interaktive sider gemmer elevens navn og svar i `localStorage`.

`manipulation.html` har den **generelle** udgave, som læser sin opsætning fra
`<body>`:

```html
<body data-store-key="man9_state_v1"
      data-modules="Modul 1: Stikprøven|Modul 2: Diagrammet|…|Blandet quiz">
```

- `data-store-key` — nøglen i `localStorage`
- `data-modules` — modulnavne til resultattabellen, adskilt af `|`

Derfor kan motoren genbruges på en ny emneside uden at blive rettet.
`statistik.html` og `funktioner-og-ligninger.html` har hver deres kopi med
hårdkodede værdier — de kan samles, hvis der skal laves en side mere.

**Markup-kontrakten**, som motoren kræver:

```
.quiz  →  .q[data-answer][data-exp]  →  .opt
          .fb                    (feedback)
          [data-score]           (badge pr. quiz)
```

Og disse id'er skal findes på siden:

`startOverlay` · `nameInput` · `ovTitle` · `ovText` · `startBtn` · `skipBtn` ·
`resetBtn` · `switchBtn` · `welcomeBar` · `welcomeHi` · `welcomeLive` ·
`progressFill` · `progressLabel` · `resultsBody` · `gradeMsg` · `finalMsg`

## Figurer

Hver opgave og hver forklaring skal have en tegning. Siger opgaven "tegn et
boksplot", skal facit vise boksplottet — ikke kun de fem tal.

Figurerne bygges med **`claude/figurer.py`**, som er et værktøj og ikke en del
af sitet (mappen er udelukket fra deploy — sitet er fortsat rene HTML-filer uden
build):

```python
import sys; sys.path.insert(0, 'claude')
import figurer as FG
svg = FG.boksplot(3, 5, 6, 9, 13, 'Talrækken 3, 5, 5, 6, 8, 9, 13')
```

| Funktion | Viser |
|---|---|
| `boksplot(min, q1, median, q3, maks, titel)` | Femtalssammendrag med kasse, median og whiskers |
| `cirkeldiagram(dele)` | Cirkeldiagram med frekvens og grader i signaturen |
| `cirkel_overflow(dele)` | Cirkel der summer til over 100 %, med synligt overlap |
| `sumkurve(graenser, hyp, aflaes, xnavn)` | Sumkurve med aflæsning af Q1, median og Q3. Returnerer `(svg, aflæsninger)` |
| `terninger(sum_)` | 6×6 udfaldsrum med de gunstige felter fremhævet |
| `areal_aerligt(side, …, forkert_faktor)` | Arealtricket: den forkerte og den ærlige tegning ved siden af hinanden |
| `loen_figur(vals, navne, enhed)` | Gennemsnit kontra median, når én værdi trækker |
| `svarprocent(N, n, tekst)` | Bortfald som prikgitter |
| `procentpoint(fra, til)` | Samme ændring i procentpoint og i procent |

Figuren sættes ind som:

```html
<div class="figur">…svg…<div class="figtekst">Forklarende tekst</div></div>
```

**Tegn aldrig en figur på øjemål.** Alle koordinater beregnes. To linjediagrammer
på `manipulation.html` påstod at vise de samme seks tal og afveg 4,8 % i niveau,
fordi de var tegnet i hånden.

## Sådan tester du

Der er ingen testsuite. Til gengæld er der to ting, der **altid** skal gøres før
et push.

### 1. Åbn siderne i en browser

Chromium og Playwright er installeret i arbejdsmiljøet:
`/opt/node22/lib/node_modules/playwright`, browsere i `/opt/pw-browsers`.
Kør ikke `playwright install`.

Tjek på hver ændret side:

- siden renderer med styling, og der er ingen JS-fejl i konsollen
- på en lektieside: **nul** multiple choice-elementer (`.opt`, `.bx`, `.mk`)
- metodeteksten er den korrekte
- ingen brudte links nogen steder på sitet
- ved print: nav og overlay skjules, og figurernes farver bevares
- der er en figur til hver opgave og hver forklaring

### 2. Regn tallene efter programmatisk

**Regn aldrig facit i hovedet.** Brug brøkregning, så afrunding ikke sniger sig
ind:

```python
from fractions import Fraction as F
```

Krav der skal holde:

- frekvenser summer til præcis 100 %
- grader i cirkeldiagram summer til præcis 360 %
- kumuleret frekvens ender på præcis 100 %
- kvartiler efter dansk skolemetode: median af hver halvdel, midterste
  observation udelades ved ulige antal
- gennemsnit går op i et helt tal, hvor det kan lade sig gøre

**Og tjek at spørgsmålet har et svar.** Et datasæt blev skiftet i uge 36, fordi
spørgsmålet "hvilke tre måneder ser flade ud" ikke havde noget svar i det første
sæt. Den slags findes kun ved at regne opgaven igennem som en elev.

Figurer tegnes ikke på øjemål — koordinater beregnes. To linjediagrammer på
`manipulation.html` påstod at vise de samme seks tal, men afveg 4,8 % i niveau,
fordi de var tegnet manuelt.

## Planlagte opgaver

Lektier udgives automatisk af Routines, så intet ligger på sitet før dagen:

| Uge | Fyrer | Id |
|---|---|---|
| 35 | 24.08.2026 kl. 08.00 dansk | `trig_01JHr8vUKSkFWdi6msBM5eMY` |
| 36 | 31.08.2026 kl. 08.00 dansk | `trig_011VkD4eyGviV1DGpejiRHsa` |

Hver flytter sin fil op i roden, tilføjer kortet på `matematik.html`, verificerer
i browser, pusher til `main` og sender facit i chatten. Ejeren får push og mail.

Skal en udgivelse aflyses eller flyttes, så **ret den Routine** — lav ikke en ny
ved siden af. De findes med `list_triggers`.

## Øvrig dokumentation

| Fil | Hvad den dækker |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Arbejdsreglerne, læses automatisk af Claude |
| [`claude/status-9klasse.md`](claude/status-9klasse.md) | Arbejdslog. **Læs den først i en ny session, og opdatér den til sidst.** |
| [`claude/lektieplan.md`](claude/lektieplan.md) | Hvilken lektie hører til hvilken uge, og hvordan de udgives |
| [`claude/opsaetning.md`](claude/opsaetning.md) | Hvordan Vercel og GitHub hænger sammen |

## Det der mangler

- **Årsplaner til samfundsfag og tysk.** Begge faner er placeholders.
- **Åbne opgaver på `funktioner-og-ligninger.html`.** Siden har kun quiz, hvor
  de to andre har Opgave A–D.
- **Lektier fra uge 37 og frem.** Der er lavet til og med uge 36. Aftalt at
  indholdet skal gennemgås, før der laves mere.
- **Fysik.** Vist som "Kommer snart" i navigationen, ingen side endnu.
- **Facit til fire filer uden indgang** — `facit/facitark-funktioner-og-ligninger.html`
  og tre ældre PDF'er. De er ikke omskrevet til det nye format.
