# Arbejdslog · 9. klasse-sitet

Sidst opdateret: 2026-09-15

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

**Samfundsfag** har årsplan og en tekstside. **Tysk** er en tom fane. **Fysik** findes ikke endnu.

## Næste skridt

1. **Quizzerne på `manipulation.html` og `funktioner-og-ligninger.html` er
   stadig ikke verificeret** — 51 spørgsmål. `statistik.html` er gennemgået
   11. september: alle 30 svar er rigtige, og de 16, der kan regnes, er
   efterregnet programmatisk.
2. **Lektier fra uge 37.** Der er lavet til og med uge 36. Aftalt at indholdet
   skal gennemgås, før der laves mere.
3. **Årsplan til tysk.** Afventer at brugeren sender den. Samfundsfag er lagt op
   15. september.
4. **Fire gamle facit-filer** i `facit/` er ikke omskrevet til det nye
   PDF-format: `facitark-funktioner-og-ligninger.html`, `facitark-manipulation.pdf`,
   `facit-lektier-manipulation.pdf`, `facit-statistik-hjemmeopgaver.pdf`,
   `facit-statistik-online.pdf`. De hører til materiale, der er erstattet.
5. **`statistik.html` mangler "tilbage til forsiden"** — den linker kun til
   `matematik.html`.

## Rettet 15. september 2026

- **Ny fane: `samfundsfag-tekster.html`.** Tre tekster lagt op som PDF med
  forsidebillede, kilde, sidetal og hvilket forløb de hører til: oversigten over
  lovprocessen, Politikens debatindlæg om Big Tech, og en side fra
  alkoholpolitik-guiden. Bygges af `claude/byg_tekster.py` — en tekst mere er én
  linje i `TEKSTER` plus en `pdftoppm`-kommando til forsiden.
- **Ophavsret:** debatindlægget er Politikens, og guiden er en andens udgivelse.
  De ligger offentligt på sitet. Skal de kun deles med klassen, skal `tekster/`
  udelukkes i `.vercelignore` og filerne sendes i Teams i stedet.

- **Årsplanen for samfundsfag er lagt op** som `aarsplan-samfundsfag.html`,
  bygget af `claude/byg_aarsplan_samf.py` ud fra lærerens egen PDF. Indholdet er
  skrevet af, ikke omskrevet. Ugernes datoer beregnes med ISO-uger, så de passer
  med matematikårsplanen, og ferier og OPO er hentet derfra, så de to planer
  siger det samme. `samfundsfag.html` er ikke længere en tom fane.
- **Opdateret efter anden udgave af planen.** Magt-temaet rammer ikke længere
  OPO: uge 1-3 Økonomi er magt, uge 8-11 Den nye verdens(u)orden, uge 13-17
  Politik er magt med Magtudredningen lagt ind, uge 18-20 opsamling. "Magt og
  medier" er ude. 19 uger teknologi, 15 uger magt.
- **Siden har fået en tidslinje** øverst — to bånd, ét pr. halvår, hvor hvert
  forløb fylder efter sit ugetal, og OPO og ferier er markeret. Tegnes af
  `FG.aarslinje()`, som er ny i figurbiblioteket og kan bruges til tyskplanen
  også. Blokke kan give en kort form af deres tekst med, så en etiket aldrig
  klippes midt i et ord.

- **Brøker står nu med vandret brøkstreg** på alle matematiksider. Syv færdige
  filer er lagt ind som de var — indholdet er gennemgået og renderet af
  brugeren og er ikke rørt her. Hver side har fået en `.frac`-komponent i sin
  egen `<style>`, så siderne stadig er selvbærende, og brøkerne er sat som
  `<span class="frac"><span>tæller</span><span>nævner</span></span>`.
- **To figurer havde brøken tegnet direkte i SVG'en** og er tegnet om: legenden
  `y = ½x + 2` på funktionssiden, hvor viewBox samtidig er hævet fra 360 til
  368, og `6 ÷ 15 = 40 %` i procentpoint-figuren på test-statistik.
- **Kontrolleret:** `claude/tjek.py` giver 0 fejl, og begge sider er åbnet i
  browser. Brøkerne står med streg og tæller over nævner, quizzen svarer med
  feedback, og der er ingen JS-fejl i konsollen.

- **Generatorerne laver nu selv brøkerne**, så hullet er lukket:
  `figurer.py` har fået `svg_broek()` og `svg_tekstlinje()`, procentpoint-figuren
  tegner `6/15` med streg i stedet for `÷`, og `koordinatsystem()` tager nu en
  signatur som liste — `('y = ', ('1','2'), 'x + 2')` — og hæver selv viewBox fra
  360 til 368, når der er en brøk i den. `byg_quiz.py` skriver forklaringerne med
  `.frac`, og `byg_test_side.py` escaper kun `&` og `"` i `data-exp`, så markup'en
  overlever. Der er ingen `÷` tilbage i `figurer.py`.
  Kontrolleret ved at bygge `test-statistik.html` om og sammenligne med den fil,
  brugeren leverede: eneste forskel er brøkens placering i procentpoint-figuren,
  5 px, og hvor `.frac`-reglerne står i stylesheetet.

## Rettet 11. september 2026

- **Quizzen på `statistik.html` er verificeret.** Alle 30 markerede svar er
  rigtige. De 16 spørgsmål med tal er regnet efter med brøkregning, resten er
  læst igennem. Ingen fejl fundet.
- **Men facit ligger aldrig på C.** 13 gange A, 17 gange B, nul gange C i alle
  30 spørgsmål. Det er et mønster, ungerne kan udnytte uden at kunne stoffet.
  De to andre sider er jævnt fordelt. Ikke rettet endnu: en omrokering ugyldiggør
  de svar, ungerne har gemt i browseren, med mindre `data-store-key` samtidig
  får et nyt versionsnummer.

- **Statistik-test til Kahoot: 30 spørgsmål, alle med illustration.** Bygget af
  `claude/byg_quiz.py`. Alle facit beregnes med brøkregning, og scriptet nægter
  at skrive filerne, hvis der er to ens svarmuligheder, et ugyldigt facit, en tid
  Kahoot ikke kender, tekst over grænserne på 120 og 75 tegn, eller et spørgsmål
  uden figur. Billederne ligger i `facit/kahoot-billeder/`, navngivet med
  spørgsmålets nummer — Kahoots import kan ikke tage billeder med.
- **Figurer må ikke røbe facit.** Tre figurer gjorde det: boksplottet skrev
  tallene og ordet "median", cirkeldiagrammet skrev procenterne, og
  svarprocent-figuren skrev svarprocenten. `boksplot()`, `cirkeldiagram()`,
  `svarprocent()` og `terninger()` har nu hver et flag til at skjule facit.
- **Rigtig fejl i `terninger()`:** billedteksten sagde altid "6 gunstige ud af
  36", uanset hvilken sum der var fremhævet. Ved sum 5 var det direkte forkert.
  Antallet beregnes nu.
- **`prikplot()` er ny i figurbiblioteket.** Spørgsmålene om median og typetal
  havde en tom tegneplads som illustration, hvilket var ubrugeligt. Nu vises
  observationerne som prikker, så typetallet kan ses som den højeste stak.
- **Testen er ikke en lektie.** Multiple choice bruges kun som quiz, jf. reglen.
- **`claude/tjek.py` kender nu serien `kahoot`** i facit-mappens navnemønster.
- **Kahoot-editoren tog ikke regnearket.** Brugerens udgave (Kahoot! GO) har kun
  slide-import: .ppt, .pptx, .key og .pdf. Derfor bygger
  `claude/byg_quiz_pptx.mjs` nu også en PPTX — ét spørgsmål pr. slide med figur,
  fire svarfelter i Kahoots farver, og det rigtige svar i slidets noter, så
  ungerne ikke kan se det. Regnearket beholdes til den udgave af editoren, der
  har regnearksimport.
- **Svarmulighederne er blandet.** Det rigtige svar stod først i alle 30
  spørgsmål, fordi det var sådan de blev skrevet. De blandes nu med en fast seed
  i `byg_quiz.py`, så alle formater får samme rækkefølge, og scriptet afviser en
  skæv fordeling. Facit ligger nu 6 gange på A, 7 på B, 10 på C og 7 på D.
- **Testen ligger nu som interaktiv side: `test-statistik.html`.** Hverken
  Kahoot (slide-import koster abonnement) eller Teams Forms virkede. Siden
  bruger den samme quiz-motor som manipulation.html — én motor i projektet — med
  30 spørgsmål i fem dele, figuren inde i hvert spørgsmål og forklaring med det
  samme.
- **Statistik til læreren uden server.** Sitet er statisk, så ungen laver til
  sidst en kode: `NAVN-27-VZXZZVB`. De seks tegn er 30 bit for rigtigt/forkert,
  det sidste er et tjekciffer. Læreren indsætter koderne på
  `test-statistik-resultater.html` og får en tabel pr. elev og pr. spørgsmål.
  **Koden indeholder ikke facit** — kun om svaret var rigtigt — så resultatsiden
  kan ligge offentligt uden at røbe noget.
  Afprøvet ende til ende i browser: 30 rigtige og en med tre fejl i nummer 3, 17
  og 28 blev afkodet præcis rigtigt, og en forfalsket kode blev afvist.
- **Forms-udgaven** er bygget af `claude/byg_quiz_forms.py` ud fra den samme
  `quiz.json`: et Word-dokument til Forms' dokumentimport og en ren tekstfil at
  kopiere fra. Det rigtige svar er markeret med en stjerne. Kahoot blev droppet,
  fordi slide-import kræver et betalt årsabonnement.
- **PPTX'en er ikke renderet visuelt.** LibreOffice bruges ikke i dette projekt,
  så den er kontrolleret geometrisk i stedet: alle figurer ligger inden for
  lærredet, og billedet overlapper ingen svarfelter. `validate.py` siger OK.

## Rettet 31. august 2026

- **Lektien til uge 36 er udgivet** (`lektier-uge36-manipulation-diagrammer.html`)
  med kort på matematiksiden. De planlagte Routines fyrede **ikke** — hverken
  uge 35 eller uge 36 blev lagt op af sig selv, så det blev gjort i hånden.
  Kontrollér de resterende Routines med `list_triggers`, før der stoles på dem.
- **Uge 35-arket blev ikke udgivet.** Ugen var passeret, og lektien ville komme
  en uge for sent. Filen ligger stadig i `kommende/`.
- **Fejl i `svarprocent()` fundet ved at kigge på siden:** figurens tredje
  tekstlinje lå præcis på viewBox-kanten og blev klippet af. Højden beregnes nu
  ud fra, om der er en tekstlinje. Rettet både i biblioteket og i uge 35-arket.

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
- **`store-tal.html`: million, milliard, billion.** Tabellen over talnavne med
  antal nuller og potens, en logaritmisk tallinje hvor SpaceX' to yderpunkter er
  sat på, og fælden: engelsk *trillion* er dansk **billion** — en faktor
  1.000.000 at tage fejl af. Tallene skrives ud af scriptet og kontrolleres mod
  eksponenten, så nullerne ikke kan tælles forkert.
- **`potenslinje()` føjet til `claude/figurer.py`.**
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
