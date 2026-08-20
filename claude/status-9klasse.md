# Arbejdslog · 9. klasse-sitet

Sidst opdateret: 2026-08-20

Læs denne fil først i en ny session, og opdatér den til sidst.

**Filoversigt, teknik, regler og testkrav står i [`README.md`](../README.md).**
Den er eneste kilde til det — hold ikke en kopi her, for to tabeller over de
samme filer driver fra hinanden. Denne fil er kun: hvad er tilstanden, hvad er
næste skridt, og hvad er lært.

---

## Tilstand

**Sitet er live** på https://www.mibelibsen.space og udgives automatisk ved push
til `main`. Deploy-kæden virker; Claudes Vercel-adgang bruges ikke.

**Matematik** har indhold: tre interaktive sider, lektier til uge 33 og 34 udgivet,
uge 35 og 36 klar i `kommende/` med planlagte Routines. Facitlister til alle
moduler og lektier ligger i `facit/` som PDF.

**Samfundsfag og tysk** er tomme faner. **Fysik** findes ikke endnu.

## Næste skridt

1. **Gennemgå matematikken på de interaktive sider.** Facit til modulopgaverne
   er nu skrevet og efterregnet, men **quizzernes** `data-answer` er ikke
   verificeret — 81 spørgsmål på tværs af de tre sider. Der er ikke lavet et
   gennemløb af, om det markerede rigtige svar faktisk er rigtigt.
2. **Lektier fra uge 37.** Der er lavet til og med uge 36. Aftalt at indholdet
   skal gennemgås, før der laves mere.
3. **Årsplaner til samfundsfag og tysk.** Afventer at brugeren sender dem.
4. **Fire gamle facit-filer** i `facit/` er ikke omskrevet til det nye
   PDF-format: `facitark-funktioner-og-ligninger.html`, `facitark-manipulation.pdf`,
   `facit-lektier-manipulation.pdf`, `facit-statistik-hjemmeopgaver.pdf`,
   `facit-statistik-online.pdf`. De hører til materiale, der er erstattet.
5. **`statistik.html` mangler "tilbage til forsiden"** — den linker kun til
   `matematik.html`.

## Rettet 20. august 2026

- **Trinvis Excel-vejledning: `excel-soejlediagram.html`.** Ungen kunne ikke lave
  et søjlediagram af SpaceX-arket, fordi tallene i K-AD er gemt som **tekst**,
  ikke som tal. Vejledningen tager de ni trin fra tekst til færdigt diagram,
  celle for celle, og forklarer hvorfor logaritmisk skala er nødvendig: væksten
  er 70.698 gange, så 2002-søjlen bliver 0,006 pixel høj ved siden af 2026.
  Ligger også som PDF i roden og er linket fra `matematik.html`.
- **`claude/figurer.py` har fået `regneark()` og `soejler_log()`.** Den første
  tegner et udsnit af et regneark med rammer og pile, så en vejledning kan vise
  præcis hvilken celle der menes. Den anden tegner søjler med lineær eller
  logaritmisk y-akse. Begge beregner koordinaterne.
- **Tre påstande blev regnet efter i stedet for skønnet.** Udkastet skrev "15 af
  19 år kan ikke ses" og "kun de sidste 3-4 søjler". Det rigtige tal er **6** —
  det er dem, hvis søjle er under 1 pixel høj ved 400 px. Tallet står nu i
  figurens titel og beregnes af scriptet.
- **`__pycache__` er taget ud af repoet** og ligger nu i `.gitignore`.

## Rettet 18. august 2026

- **`claude/tjek.py` er lavet.** Ni kontroller, én pr. fejltype fra projektets
  historie. Kør det før hvert push. Det fandt med det samme, at årsplanens to
  udgaver kan drive fra hinanden — det skete tre gange på én dag.

- **`funktioner-og-ligninger.html` var det største hul** — kun quiz, ingen åbne
  opgaver, to figurer. Den har nu Opgave A–D med 26 delspørgsmål, tre nye
  figurer, og quiz-motoren er gjort generel som på manipulation.
- **Lektier til uge 38, 39 og 41** er lavet og planlagt. Dermed er der lektier
  til hele blok 1 og blok 2 så langt, som sidernes indhold rækker.
- **Illustrationer på selve sitet.** De fire diagramtyper på statistik.html har
  fået et eksempel hver, og kildekritik-modulet har fået den afskårne y-akse
  tegnet.
- **Endnu en talfejl fundet ved at tegne:** siden skrev, at to søjler på 102 og
  105 ser "dobbelt så større" ud med afskåret akse. De ser **2,5 gange** så høje
  ud, og den reelle forskel er **2,94 %**. Rettet, og begge tal står nu i figuren.
- **Lektiearkene uddeles som PDF uden facit** fra `lektieark/`, navngivet uden
  ordet facit. Mappen er udelukket fra deploy.

## Rettet 17. august 2026

- **Der manglede figurer overalt.** Facitlisterne gav kun tal, selvom fem opgaver
  siger "tegn et boksplot / en sumkurve / et cirkeldiagram". Alle elleve
  facitlister har nu tegningerne, og lektiearkene har fået tegnepladser — tomme
  akser og en tom cirkel med gradmarkeringer — så de kan printes og udfyldes uden
  at facit røbes. Figurbiblioteket ligger i `claude/figurer.py`.

- **`manipulation.html` hentede `/style.css` og `/app.js` fra sitets rod** og lå
  ustylet med død quiz. Begge er nu inline, og motoren er gjort generel via
  `data-store-key` og `data-modules`.
- **Facit lå offentligt på sitet** — fem filer kunne hentes af enhver, der gættede
  adressen. Flyttet til `facit/` og udelukket i `.vercelignore`.
- **Hjemmeopgaverne var multiple choice.** `statistik-hjemmeopgaver.html` (30
  afkrydsnings- og 5 åbne opgaver) er erstattet af lektieark med kun åbne opgaver.
- **De to linjediagrammer på `manipulation.html` viste ikke de samme tal**, selvom
  siden påstod det: venstre lå på ~100, højre på ~105 — 4,8 % afvigelse, fordi de
  var tegnet manuelt. Begge er nu genberegnet fra ét datasæt, og tallene står i en
  tabel på siden, så eleven kan regne efter uden at måle på pixels.
- **Dubletmappen `model-fra-anden-chat/`** er slettet. Dens tre PDF'er var unikke
  og er flyttet.
- **`main` er oprettet og sat som default-branch.** Repoet var helt tomt ved
  sessionens start.
- **Den forældede `claude/deploy.md` er slettet.** Den beskrev en blokering, der
  ikke findes længere.

## Hvad der gik galt, og hvad det lærte

Dagen før gik med fejlslagne forsøg på at automatisere deploy. Årsagen var, at
Claude deployede **gennem** Vercels API, hvor adgangen kan oprette ting men
hverken læse dem igen eller udgive. Hvert forsøg lykkedes halvt, og det næste
byggede oven på noget halvfærdigt. Der blev oprettet omkring ti Vercel-projekter
til ét site.

Tre vaner kom ud af det, og de står som regler i `README.md`:

1. **Gæt ikke på en adresse.** Skriv linket ud, og ret det hvis det fejler. En
   klikvej er ikke et acceptabelt alternativ — brugeren har bedt om dybe links
   mange gange.
2. **Regn efter i stedet for at antage.** Både facit og figurer. To reelle fejl
   blev fundet præcis sådan: linjediagrammerne ovenfor, og et spørgsmål i uge 36
   der ikke havde noget svar i det oprindelige datasæt.
3. **Sig hvad du fandt, frem for at bygge videre på gætværk.** Det gælder også de
   planlagte Routines, som har den instruks skrevet ind.
4. **Lad maskinen holde øje.** Alt hvad der findes to steder, driver fra
   hinanden. `claude/tjek.py` sammenligner dem automatisk — udvid det, når en
   ny dublet opstår, i stedet for at love at huske det.
5. **Vis det, i stedet for kun at skrive det.** Der skal være en figur til hver
   opgave og hver forklaring — også i facit. Brug `claude/figurer.py`, og beregn
   koordinaterne.
