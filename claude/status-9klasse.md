# Arbejdslog · 9. klasse-sitet

Sidst opdateret: 2026-09-22

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

**Samfundsfag** har årsplan og en tekstside. **Tysk** har projektet *Ung i
Tyskland* (`tysk-spoergeskema.html`) men ingen årsplan. **Fysik** findes ikke endnu.

**Spørgeskemaet til Tyskland virker fra ende til anden (22.9.)**: 23 unger
har koder og kort (`spoergeskema/qr-kort-a6.pdf`, A4-plakaterne findes også).
`/u/<kode>` sender videre til det fælles Google Form med navnet i feltet
`Code` (24 redirects i `vercel.json`, tjekket live). Skemaet er udgivet, uden
e-mail-indsamling, og svarene lander i fanen `Svar` i regnearket. Siden
`tysk-spoergeskema.html` viser ungernes spørgsmål fra arket live og siger nu,
at koden kommer som et kort (A6).
**Google-siden af sagen:**
- regneark med fanen Unger og optælling:
  https://docs.google.com/spreadsheets/d/1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY/edit
- ungernes spørgsmål skrives i et fælles ark (delt med alle med linket), som
  siden læser via gviz-CSV: https://docs.google.com/spreadsheets/d/1tV_rBMFwAtc8jQUXqP32TBOSEg52ZBQ05T-MIrfAK-Y/edit
  Kolonnerne til svarmuligheder er lavet (22.9. stod der Antwort 1, 2, 4, 5 —
  Antwort 3 manglede, og de to Auswahl-linjer havde ingen muligheder endnu).
  Forslagsformularen (1DfEjbE50…) er droppet og kan slettes.
- `spoergeskema/byg_formular.gs` bygger skemaet af arket (Apps Script i arket,
  funktionen bygSkema). Brugeren kører det igen, når klassen har skrevet sine
  spørgsmål; det beholder feltet Code, så linkene og koderne holder.
- Test af et rigtigt svar er brugerens: send aldrig prøvesvar til skemaet.
- spørgeskemaet (tomt): https://docs.google.com/forms/d/1_zEW7e1bvwL46TeywzPD9S3f8NzQ8CwDco62mWMWUgc/edit
- teksterne til formularerne: https://docs.google.com/document/d/1h96ppA_vi6fnoye0KmNs5RWzKT5Zoh-YOCsrhBMM4TQ/edit
Brugerens eget, tomme ark *Tysk spørgeskema* (18Ns9i35…) kan slettes.
Når linkene kommer: sæt dem i `spoergeskema/opsaetning.json`, kør
`python3 claude/byg_spoergeskema.py`, push. Plakaterne behøver ikke trykkes om.
Vejledningen står i `vejledning/spoergeskema-tyskland.md`.

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

## Rettet 22. september 2026

- **Plastik-forløbet: brød i stedet for agurk, "Frysepose" og "Madpapir".**
  Rettet i `claude/byg_feature_plastik.py`; siden, ungearket (PDF) og
  vejledningen (PDF + Word) er bygget om. Vejledningen minder om at bruge frisk
  franskbrød, for tørt brød har ikke meget vand at miste.

- **Reklame-algoritmen: `algoritme.html` på `/algoritme`.** Brugerens egen
  fil, lagt op uændret som selvstændigt program: intet kort på forsiden, ingen
  links til resten af sitet, rewrite i `vercel.json`. Siden henter skrifttyper
  fra Google Fonts, hvilket tjekket tillader (forbuddet gælder sitets rod).
  Undtaget i figurtjekket, fordi pointstakken tegnes med div'er.
  QR-kode til adressen i `materiale/qr-algoritme.svg/.png/.pdf`, bygget af det
  nye `claude/byg_qr.py`.

- **Ungernes spørgsmål samles i et fælles ark, ikke en formular.** Arket
  *Ung i Tyskland – jeres spørgsmål* er delt med alle med linket; kolonner
  Navn · Deine Frage · Antworttyp · Antwortmöglichkeiten · Kommentar.
  Projektsiden henter arket som CSV via `/gviz/tq?tqx=out:csv` (Google sender
  CORS-header til sitets origin, ikke til `null`, så det kan kun testes live)
  og viser hvert spørgsmål som et kort; eksempellinjen springes over.
  Brugeren sætter selv rullemenuen på Antworttyp. Drev-adgangen kan ikke
  uploade xlsx (afvises), så validering kan ikke lægges ind derfra.
- **`spoergeskema/byg_formular.gs`**: Apps Script, der bygger Google-skemaet
  af arket (Code først, typer efter Antworttyp, alder og køn sidst), kobler
  svarene til fanen Svar, udgiver og skriver linkene i fanen Links. Køres af
  brugeren ved en computer; scriptet er kun syntakstjekket, ikke kørt.
- **Nye Google Forms skal udgives** (knappen Udgiv), før andre kan åbne dem —
  ellers "This document is not published". "Indsaml e-mailadresser" står som
  standard til *Bekræftet* og tvinger login; skal slås fra.
- **Spørgeskema med personlige QR-koder: `tysk-spoergeskema.html`.** Ét
  Google-spørgeskema, ens for alle, med et forudfyldt felt `Code`. Hver ung har
  sin egen adresse `/u/<kode>` på sitet, som `vercel.json` sender videre til
  skemaet med navnet i linket — så hvert svar tæller på den rigtige ung, og alle
  svar ligger i ét ark. Koderne peger på sitet og ikke på Google, så plakater
  kan trykkes før skemaet er færdigt, og skemaet kan skiftes uden nye plakater.
  `/u/eksempel` fører tilbage til siden og bruges til at prøve scanningen.
- **`claude/byg_spoergeskema.py`** bygger siden, redirects, `unger-links.tsv`
  og PDF'er med plakater (A4, én pr. ung) og kort (A6, fire pr. ark). Under
  hver kode står navnet, Dannebrog og en tysk tekst om, at klassen samler viden
  om at være ung i Tyskland for at sammenligne med Danmark. Mappen
  `spoergeskema/` er udelukket fra deploy og lagt ind i `tjek.py`.
- **`claude/qr.py` er en QR-koder i ren Python** — ingen pip i en frisk
  session. Krydstjekket mod segno: 896 koder (version 1–10, alle niveauer og
  masker) er identiske bit for bit, og zxing-cpp læser dem tilbage. To fejl
  fanget undervejs af tjekket: GF(256)-multiplikationen reducerede på den
  forkerte bit, og reservationen til formatinfo overskrev timing-mønstret.
  segno selv afviger fra standarden med et ekstra nul-kodeord efter
  terminatoren; selvtesten normaliserer det.
- **`claude/html_til_pdf.mjs`** gengiver HTML som PDF med Chromium og
  sidestørrelse fra `@page`. Kan bruges af alle byggescripts.
- **Nyt i figurbiblioteket: `soejler()`**, et almindeligt søjlediagram med
  tallet oven på hver søjle.
- Kort til projektet på `tysk.html` og forsiden. Vejledning til den voksne i
  `vejledning/spoergeskema-tyskland.md` med links til Forms og Sheets.

## Rettet 21. september 2026

- **KontikAir: `kontikair.html` med tre papirflyvere.** Pilen (længde),
  Svæveren (svævetid) og Bumleren (loops, foldet af et ark på tværs). Hver har
  en A4-skabelon med foldelinjerne trykt på, og en vejledning trin for trin.
- **`claude/byg_kontikair.py` folder papiret i stedet for at tegne det.**
  Papiret er en polygon; hver fold klipper polygonen i to, spejler klappen i
  foldelinjen og gør resten til den nye silhuet. Foldene defineres af tre
  primitiver — kant på linje (vinklens halveringslinje), punkt på punkt
  (midtnormalen) og parallel — og scriptet tjekker, at en klap, der skal foldes
  indad, faktisk lander inde på papiret. Både skabelonernes foldelinjer og
  trintegningerne kommer af de samme beregninger.
- **Alle folder går bagud.** Det er ikke kosmetik: derfor bliver ingen
  foldelinje dækket af en klap undervejs, og derfor kan *hver eneste* fold —
  også vingefolderne, der laves efter at flyveren er foldet sammen — trykkes
  på det flade ark. Den trykte side ender udvendigt på den færdige flyver.
- **`vercel.json` er ny** med én rewrite, så `/kontikair` virker uden `.html`.
  Interne links bruger stadig `.html`, så `claude/tjek.py` kan følge dem.
- Skabelonerne gengives som PDF med sidestørrelse sat i millimeter, og
  målt efter bagefter: 210,2 × 297,3 mm (Bumleren på tværs). Der står på arket,
  at det skal printes i 100 %.

## Rettet 19. september 2026

- **Sløjdopskrift på en katapult: `katapult.html`.** Katapult på fire hjul med
  kastearm, elastik og en udløser, der hives bagud. Bygget af
  `claude/byg_katapult.py`, hvor hele mekanikken er ét sæt tal i `M`: styklisten,
  tegningerne og teksten regnes ud af de samme mål.
- **Scriptet nægter at skrive filerne, hvis mekanikken ikke hænger sammen.**
  Der er asserts på, at stoppinden standser armen ved 45° (den skal sidde
  forskudt fra 45°-linjen, fordi den rammer armens *overside*, ikke dens
  midterlinje), at elastikken strækkes nok, at den ikke skurer mod stoppinden,
  at halen ikke lander på udløserstangen, og at hullerne ligger inde i træet.
  Stoppindens placering blev regnet forkert i første forsøg — armen ville være
  standset ved 32°, og kuglen var gået opad.
- **Nyt i figurbiblioteket: `Rids`.** En målsat teknisk tegning i millimeter med
  `rekt`, `poly`, `hul`, `pind`, `skive`, `bue`, `maal_v`, `maal_l`,
  `maal_skra`, `vinkel`, `note` og `maerke`. Målene tegnes af de samme tal som
  delene, så et mål ikke kan komme til at sige noget andet end stregen.
- **`claude/byg_vejledning_docx.py` er gjort generel.** Den tager nu kilde og
  udfil som argumenter og gengiver alle figurer i dokumentet, ikke kun den
  første. Både plastik- og katapultvejledningen bygges af den.

## Rettet 18. september 2026

- **Feature til Naturfagsuge 2026: `feature-plastik-og-foedevarer.html`.**
  Forløb på 3½ time om plastik og fødevarer med tre forsøg: emballagetest med
  vejning og procentregning, plastsortering ved flyde-synke i vand og mættet
  saltvand, og hjemmelavet bioplast af kartoffelmel. Kortet ligger på forsiden
  med mærkatet Feature.
- **Ungeark og vejledning bygges af `claude/byg_feature_plastik.py`.**
  Ungearket ligger åbent i `materiale/`; vejledningen ligger i den nye mappe
  `vejledning/`, som er udelukket fra deploy — den hedder ikke facit, for det er
  den ikke, men den indeholder forventede resultater og hører til den voksne.
  Rammen er **44 unger på tre hold** (15, 15 og 14), ét hold om dagen, fire
  grupper pr. dag — i alt 12 grupper. Indkøbslisten regnes ud fra det, og
  densitetstabellen kontrolleres mod massefylderne: scriptet nægter at skrive
  filerne, hvis fx PS står som flydende i vand.
- **Fejl fanget i indkøbslisten:** saltet stod som 400 g *pr. gruppe* og gav
  4,8 kg. Saltvandet er én liter **pr. dag**, ikke pr. gruppe. Listen har nu en
  egen tabel over det, der hører til dagen — 1.080 g salt i alt.
- **Nyt i figurbiblioteket:** `tomt_soejlegitter()` til at tegne søjler i hånden.
  Og `procesdiagram()` vælger nu tekstfarve efter feltets lyshed — pausefeltet
  havde hvid tekst på lys grå og kunne ikke læses.
- **`claude/tjek.py` kender serien `laerer`** i facit-mappens navnemønster.
- **Ingen klokkeslæt i det, ungerne ser.** Tid og pauser styres på dagen, så
  sitets side og ungearket har programmet som nummererede trin uden tider, og
  "urørt i to timer" er skiftet til "til de vejes igen". Vejledningen til den
  voksne beholder programmet minut for minut — `byg_feature_plastik.py` bygger
  begge varianter af samme `PROGRAM`, så de ikke kan komme til at sige noget
  forskelligt om rækkefølgen.
- **Forsidens felt er kortet ned** til "Naturfagsuge 2026 · Plast og fødevarer –
  værksted".
- **Vejledningen findes nu også som Word-fil.** `claude/byg_vejledning_docx.py`
  læser den samme HTML, som PDF'en gengives fra, og bygger
  `vejledning/vejledning-plastik-og-foedevarer.docx` ud af overskrifter, afsnit,
  tabeller og procesdiagrammet (gengivet som PNG). Ingen tekst skrives af i
  hånden, så Word-filen og PDF'en kan ikke drive fra hinanden. Mappen er fortsat
  udelukket i `.vercelignore`.
- **Ordlyden rettet i hele feature-forløbet:** "Naturfagsfestival" hedder nu
  **Naturfagsuge 2026** (forside, side, ungeark, vejledning), der står **unger**
  og ikke elever, og **læreren** er skiftet ud med **den voksne** i rette
  bøjninger — vejledningen hedder "Vejledning til den voksne". Elevarket er
  omdøbt til `materiale/ungeark-plastik-og-foedevarer.pdf`, og begge PDF'er er
  gengivet på ny.

## Rettet 16. september 2026

- **Lektien til uge 38 er udgivet** — Opgave A og B om ligninger.
- **Udgivelse er ikke længere automatisk.** De to sidste udgivelses-Routines
  (uge 39 og 41) er slettet. Klassens tempo svinger i forhold til årsplanen, så
  læreren afgør selv hvornår en lektie gives — og Routines fyrede alligevel
  ikke pålideligt: uge 35, 36 og 38 måtte udgives i hånden.
  I stedet kommer der en **mandagsmail**, `trig_01X2DGTRBWt12ZNRiuZUD8eo`, der
  kun fortæller hvad der ligger klar. Den har direkte besked på ikke at udgive.
- **"og CAS" er væk fra lektiearkenes overskrift** — ungerne ved ikke hvad det
  betyder. Forkortelsen står stadig i årsplanen og i læringsmålene, hvor den
  hører hjemme.
- **To nye opslag på matematiksiden:** `regnepyramiden.html` og
  `broekregning.html`, begge med figurer, fælder og printknap.

## Rettet 15. september 2026

- **Ny fane: `samfundsfag-tekster.html`.** Tre tekster lagt op som PDF med
  forsidebillede, kilde, sidetal og hvilket forløb de hører til: oversigten over
  lovprocessen, Politikens debatindlæg om Big Tech, og en side fra
  alkoholpolitik-guiden. Bygges af `claude/byg_tekster.py` — en tekst mere er én
  linje i `TEKSTER` plus en `pdftoppm`-kommando til forsiden.
- **Lovprocessen er nu en side, ikke en PDF:** `lovprocessen.html`, bygget af
  `claude/byg_lovprocessen.py`. Procesdiagrammet tegnes af den nye
  `FG.procesdiagram()`, de ni trin er uddybet, der er en ordliste, og siden kan
  printes — den fylder fem A4-sider.
- **Rettet undervejs:** PDF'en skrev, at to-dages-reglen står i grundlovens
  § 41. Grundloven kræver tre behandlinger; at der skal gå mindst to dage
  mellem dem står i Folketingets forretningsorden. Siden siger det nu korrekt.
- **To slags materiale, to mapper.** `materiale/` er vores eget og ligger
  åbent på sitet — lovprocessen ligger der med forside og kan åbnes af enhver.
  `tekster/` er tekster med begrænset rettighed og er udelukket i
  `.vercelignore`; de vises kun som overskrift med et link til klassens Teams.
  `claude/tjek.py` kontrollerer, at `tekster/` er udelukket.
  `byg_tekster.py` afviser en tekst, der både har `fil` og `link`.

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
