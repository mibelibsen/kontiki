# Arbejdslog · 9. klasse-sitet

Sidst opdateret: 2026-11-11

Læs denne fil først i en ny session, og opdatér den til sidst.

**Filoversigt, teknik, regler og testkrav står i [`README.md`](../README.md).**
Den er eneste kilde til det — hold ikke en kopi her, for to tabeller over de
samme filer driver fra hinanden. Denne fil er kun: hvad er tilstanden, hvad er
næste skridt, og hvad er lært.

---

## Tilstand

**Sitet er live på https://321flyv.com** og udgives automatisk ved push til
`main`. Deploy-kæden virker; Claudes Vercel-adgang bruges ikke til ændringer.

**Domænet skiftede 3.11.**, fordi skolens webfilter blokerede
`mibelibsen.space`. Det gamle domæne viderestiller midlertidigt (307) året ud
og **skal fjernes fra projektet efter 31.12.2026**, så brugeren kan bruge det
til noget andet. Der ligger en påmindelse til 4.1.2027. Sidehovedet hedder
**321flyv · 9. klasse**; navnet «Mibelibsen» er væk fra sitet.

**Matematik** har mest indhold: tre interaktive sider (statistik, manipulation,
funktioner og ligninger), **Matematik klip** med seks klippeark (areal,
rumfang, overflade, Pythagoras, trigonometri, ligninger), **Intro til
GeoGebra** med elleve skærmbilleder fra den rigtige app, opslagssider,
Undervisningsministeriets *Matematiske formler og fagord*, og lektier til og
med uge 44. Facit til alle moduler og lektier ligger i `facit/` som PDF og
kommer aldrig på sitet.

**Dansk** har `/dansk` med tre øvelsessæt i skriftlig fremstilling og en
essayvejledning. **Ingen side linker dertil** — det var med vilje. Dertil
spillet **Fyrtøjet** på `/fyrtoejet`, som har et kort på forsiden.

**Samfundsfag** har årsplan og en tekstside. **Tysk**: *Ung i Tyskland* er
afsluttet med 170 besvarelser; resultaterne blev til en PDF, og
segmentopgaven (`tysk-segmenter.html`) ligger klar til de to Peter'e. Der er
ingen årsplan i tysk — den er droppet. **Fysik** har naturfagsugens materiale.

**FP9-prøverne 18.-22. januar 2027** ligger som kalenderfil i
`vejledning/fp9-proever-januar-2027.ics`.

### Spørgeskemaet til Tyskland · afsluttet

23 unger fik koder og kort; `/u/<kode>` sender videre til det fælles Google
Form med navnet i feltet `Code` (24 redirects i `vercel.json`). De printede
plakater peger på det **gamle** domæne — en viderestilling redder dem ikke på
skolens net, for filteret blokerer forespørgslen, før viderestillingen sendes.
Skal de bruges igen, printes de forfra med
`python3 claude/byg_spoergeskema.py`, som nu bygger dem med 321flyv.com.

- regneark med fanen Unger og optælling:
  https://docs.google.com/spreadsheets/d/1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY/edit
- ungernes spørgsmål:
  https://docs.google.com/spreadsheets/d/1tV_rBMFwAtc8jQUXqP32TBOSEg52ZBQ05T-MIrfAK-Y/edit
- spørgeskemaet: https://docs.google.com/forms/d/1_zEW7e1bvwL46TeywzPD9S3f8NzQ8CwDco62mWMWUgc/edit
- `spoergeskema/byg_formular.gs` bygger skemaet af arket (Apps Script, funktionen
  bygSkema). Test af et rigtigt svar er brugerens: send aldrig prøvesvar.
- Vejledningen står i `vejledning/spoergeskema-tyskland.md`.

## Næste skridt

1. **Fjern `mibelibsen.space` fra `kontiki-9klasse` efter 31.12.2026.**
   Ikke slette domænet fra kontoen — kun tage det af projektet, så det kan
   bruges til noget andet. Påmindelsen fyrer 4.1.2027.
   https://vercel.com/mibelibsens-projects/kontiki-9klasse/settings/domains
2. **Lektier fra uge 37.** Der er lavet til og med uge 36 plus uge 38, 39 og
   44. Aftalt, at indholdet skal gennemgås, før der laves mere.
3. **Fire gamle facit-filer** i `facit/` er ikke omskrevet til det nye
   PDF-format: `facitark-funktioner-og-ligninger.html`,
   `facitark-manipulation.pdf`, `facit-lektier-manipulation.pdf`,
   `facit-statistik-hjemmeopgaver.pdf` og `facit-statistik-online.pdf`. De to
   sidste bærer stadig navnet «Mibelibsen», fordi de ingen byggescript har.
   De hører til materiale, der er erstattet.
4. **Vercel-oprydning er parkeret af brugeren** (20.10.): `mibelib-space` og
   ti andre tomme projekter. Sletning kan kun ske i dashboardet —
   `get_project_deletion_link` svarer `requires_user_action`.
5. **Fyrtøjet linker ikke til `/dansk`.** Spillet står for sig selv med et
   kort på forsiden. Hører det til dansksiden, skal den side have et sted til
   litteratur — den er i dag ren skriftlig fremstilling.

## Lavet 6. oktober 2026 · samfundsfag

- **`digital-socialisering.html` er bygget** — dataark til forløbet i uge 40 og
  41, som årsplanen kalder *Digital socialisering blandt unge*. Resumé i fem
  punkter, otte dataafsnit med figur og tabel, et tomt søjlegitter til klassens
  egne tal fra Hamborg, en kildekritisk boks og to film. Bygges af
  `claude/byg_digital_socialisering.py`.
- **Hver kilde er åbnet og læst**, ikke refereret fra et referat, og **alle 15
  links er tjekket og svarer 200**. Dato og stikprøve står ved hvert tal.
- **Intet bag betalingsmur.** Kristeligt Dagblad og Information blev valgt fra;
  PISA-tallet står i stedet i ministeriets egen frie nyhed, som også har de to
  bedste tal: 3,8 timer mod OECD's 2, og 72 % mod 16 %.
- **En kilde måtte byttes.** Den australske myndighed eSafety kan ikke nås fra
  containeren — alle deres adresser giver 000. DR's dækning blev brugt i stedet,
  og den havde endda bedre tal med: tre måneder efter forbuddet brugte 8 ud af
  10 stadig sociale medier, og andelen med egen konto faldt kun fra 52 til 42 %.
- **Alle 111 quizspørgsmål er regnet efter (21.10.).** Facit er rigtigt i
  dem alle — statistik (30), manipulation (25), funktioner og ligninger (26)
  og test-statistik (30). De fem, der afhænger af en figur, er tjekket mod
  figurens egne tal.
  **To spørgsmål pegede på en figur, der ikke kunne aflæses.** "Hvilket
  interval har flest unger i histogrammet?" og "Hvad er typetallet ifølge
  søjlediagrammet?" brugte `mini_histogram` og `mini_soejler` — pyntefigurer
  på 100×100 uden akser, uden tal og uden en eneste tekst. Svarene var
  rigtige; spørgsmålene var ikke til at besvare uden at gætte, at tredje
  søjle svarede til tredje svarmulighed. De har nu rigtige figurer.
  Ny funktion i `figurer.py`: **`histogram`** — søjler der rører hinanden,
  med intervalgrænserne på x-aksen. Det er forskellen på et histogram og et
  søjlediagram, og den skal kunne ses. Pyntefigurerne bliver stående; de
  duer til at illustrere et afsnit, bare ikke til at aflæse.
- **GeoGebra-vejledningen er koblet på matematikken (3.11.).** Den var
  udgivet og ulinket, mens brugeren testede den selv. Nu linker
  `matematik.html` til den med et kort, og `funktioner-og-ligninger.html`
  har en tip-boks lige før **opgave C** og et link i **opgave D** — præcis
  de to opgaver, vejledningen er skrevet til. Siden har selv fået en vej
  tilbage: *Opgaverne* i menuen og *Tilbage til opgaverne* i toppen. Før
  havde den ingen udgang overhovedet.

- **GeoGebra-vejledning til opgave C og D (21.10.) — byggede som ULINKET.**
  `geogebra-lineaere-funktioner.html` i roden, bygget af
  `claude/byg_geogebra.py`. **Ingen side linker til den.** Den kan kun nås på
  `mibelibsen.space/geogebra-lineaere-funktioner.html`, så brugeren kan sidde
  og nørkle med den i en rigtig browser, før den kobles på matematik.html og
  funktioner-og-ligninger.html. **Ulistet er ikke privat** — har man
  adressen, kan man læse den. `tjek_links` kræver kun, at links peger på noget,
  der findes, så en ulinket side består tjekket.
  **Kommandonavnene er prøvet af i GeoGebra Classic på dansk, ikke husket.**
  De hedder `Linje`, `Hældning`, `Rod` og `Skæring`. **Der findes ingen
  `Nulpunkt`-kommando** — den hedder `Rod`, selv om vi siger nulpunkt i
  timen. Det stod der i første udkast, og det ville have kostet en lektion.
  API'et (`ggbApplet.evalCommand`) tager kun engelske navne, men
  algebravinduet *viser* de danske — det er sådan, de blev slået fast.
  **Ingen facit på siden:** alle eksempler bruger y = 2x + 1 og y = x + 4,
  ikke opgavernes egne tal. Skriver man opgave C's to kvitteringer ind i
  GeoGebra, står svaret på skærmen med det samme, og det skal ungerne selv
  nå frem til.
  Siden henter CSS fra `funktioner-og-ligninger.html` og skal derfor bruge
  **den sides header** (`.top-inner` og `.jump`, ikke `.tabs`) og `.btn`,
  ikke `.btnlink`.
- **Quizmotoren: et fejlklik låste spørgsmålet for altid (rettet 21.10.).**
  Svarede man forkert, blev alle knapper spærret, og det eneste, der kunne
  låse op, var *Nulstil mine svar* — som sletter hele sidens svar. Svaret
  blev gemt i localStorage, så "Ikke helt" kom igen ved hver genindlæsning.
  Oven i det stod der kun "Ikke helt" og derefter det rigtige regnestykke:
  *"Ikke helt. y = 2·3 + 1 = 7."* Når 7 står på en af knapperne, ser siden
  ud til at modsige sig selv. Nu står der, hvilket bogstav der var det
  rigtige, og der er en **Prøv igen**-knap, der kun nulstiller det ene
  spørgsmål.
  Motoren er kopieret ind i fire sider — `statistik.html`,
  `manipulation.html`, `funktioner-og-ligninger.html` og
  `test-statistik.html` — og de er rettet alle fire. Ingen af dem bygges af
  et script, så en rettelse i motoren skal laves fire steder.
- **Samtaleark til skole-hjem-samtaler (21.10., omskrevet 22.10.).**
  `claude/byg_samtaleark.py` bygger `vejledning/skolehjemsamtale.pdf` — to
  A4-sider pr. barn til en samtale på en halv time, fagligt fokus. Side 1:
  tidsbåndet som figur, felter til barn og dato, og et skema med fagene —
  standpunkt og barnets vurdering. **Kun fire fag (26.10.):** dansk,
  matematik, samfundsfag og idræt. Overskriften tæller selv, så der
  ikke kommer til at stå "otte" dagen efter, listen laves om. Side 2: to tomme **fokusfag**-blokke
  med standpunkt (faglige områder), mål, og *hvad skal der til* delt i
  **I skolen · Hjemme · Barn**, plus aftaler.
  **Tidsbåndet har ingen tal, og det er med vilje.** Den blå blok "Barnet
  selv" er præcis lige så bred som de tre andre tilsammen og ligger
  forrest. Det står ingen steder på arket, at barnet skal have halvdelen af
  tiden — figuren viser det, og det er nok til at skubbe samtalen den vej.
  Et minuttal på en farve ville gøre båndet til et skema, man skal
  overholde. `figurer.py`-funktionen `tidsplan` har derfor `tal=False`.
  Ingen numre ud for fagene i fokusblokkene: de to fag vælges under
  samtalen, og et nummer ligner en rangordning.
  **Skrivelinjerne tegnes én ad gangen**, ikke som et gentaget
  baggrundsmønster. Mønsteret blev klippet af feltets højde, så der stod
  tre linjer i den ene blok og to i den anden — præcis samme felt.
  **Udfyldelig PDF (27.10.).** De 34 skrivepladser er rigtige
  formularfelter, saa barnet selv kan skrive i kolonnen *Barnets
  vurdering*. Layoutet er uændret — felterne ligger oven på de streger,
  der var der i forvejen. Målene gættes ikke: hvert felt får to usynlige
  markører i hjørnerne, PDF'en bygges, og `pdftotext -bbox` siger
  bagefter, hvor de landede. `claude/pdf_felter.py` lægger dem ind med
  pypdf, som kun findes i python3.13 her.
  **Første forsøg lavede en helt ny side 1 til barnet** med nye
  spørgsmål. Det var for meget: brugeren ville have arket, som det var,
  bare udfyldeligt. Lav ikke side 1 om igen.
  **PDF'en er ikke i git** (`.gitignore`). Den er en bygget fil, og et
  udfyldt ark er vurderinger af et navngivet barn — scriptet er kilden.
- **Grupperne til fredag i uge 44 (27.10.).** Renskrift af den håndskrevne
  seddel "Info til 9. kl": ti grupper, 35 unger fra 8. og 9. klasse, til når
  6. og 7. klasse kommer på besøg **fredag kl. 11–12**. Dagen passer med
  ugeplanen på `plastik-stand.html`; tidspunktet er nyt.
  Navnelisten står i `claude/byg_grupper.py`, PDF'en er bygget og ikke i git.
  **Tre grupper er på to (1, 9 og 10)**, selvom rammen siger tre til fem.
  Det er sagt til brugeren, ikke rettet — det er hendes opdeling.

- **Vejledning: fra stående til liggende video (29.10.).** En elev havde
  en video, der skulle være vandret. **Første udgave ramte ved siden af:**
  "vendes horisontalt" blev læst som spejlvending, men det var orientering.
  Vejledningen hedder nu `vejledning/staaende-til-liggende-video.pdf` og
  skiller de to problemer ad, fordi de ligner hinanden og har hver sin knap:
  1. **Billedet ligger på siden** — videoen er optaget rigtigt, bare gemt
     forkert vendt. Den skal roteres en kvart omgang.
  2. **Billedet står rigtigt, men er højt og smalt** — den skal have et nyt
     format, og **man skal vælge**: enten beskæres top og bund væk, eller
     også kommer der bjælker i siderne. Der er ikke en tredje mulighed, og
     figuren viser netop det valg.
  Tre maskiner hver gang: Billeder på iPad, QuickTime/iMovie på Mac,
  Clipchamp på Windows. Trinene er slået efter hos Microsoft, ikke husket.
  Bygges af `claude/byg_videoformat.py` som PDF og Word; teksten står ét
  sted. `claude/svg_til_png.mjs` gengiver figuren, så Word-udgaven viser
  den samme tegning.
  **Word tæller ikke selv:** stilen List Number deler én tæller mellem alle
  lister i dokumentet, så anden liste begyndte ved 5. Numrene skrives som
  tekst med hængende indrykning.

- **Dansk på `/dansk` (3.11.) — UDGIVET, men ULINKET.** Fem sider i roden,
  bygget af `claude/byg_dansk.py`, med omskrivninger i `vercel.json`:
  `/dansk`, `/dansk/saet-1`, `/dansk/saet-2`, `/dansk/saet-3` og
  `/dansk/essay`. **Ingen side på sitet linker til dem**, de har `noindex`,
  og de står hverken i menuen eller på forsiden. **Ulistet er ikke privat.**
  **Sæt 1 og 2 er brugerens egne.** De lå på et andet Vercel-projekt,
  `mibelib-space.vercel.app/dansk`, som ikke er et repo, vi har. Indholdet
  er hentet derfra ord for ord — fire opgaver pr. sæt, forlæg,
  dr.dk-kilder, vurderingskriterier. **Alle seks dr.dk-links er tjekket og
  svarer 200.** Den gamle side henter `/style.css` fra roden; her står
  CSS'en inline, som reglen siger.
  **Sæt 3 er skrevet herfra** over brugerens tre emner — drømme om fremtid
  og uddannelse (essay), sociale medier og forventningspres (debatindlæg),
  fremtidens arbejdsmarked med AI (mundtligt oplæg) og året efter
  (fortælling). Samme form som de to andre: forlæg, situation, rolle,
  forberedelse og fire krav med udsagnsord.
  **To blindgyder først.** Første forsøg antog, at der ingen dansk-side
  fandtes, og byggede en ny med fane i menuen og kort på forsiden. Andet
  forsøg opfandt Sæt 1 og 2. Begge dele er rullet tilbage. **Spørg efter
  adressen, når brugeren taler om en side, der ikke er i repoet** — den kan
  ligge på et andet Vercel-projekt.
  Tre figurfunktioner i `figurer.py`: `konkret_abstrakt` (stilen nede,
  kronikken oppe, essayet op og ned), `afsaet` (tre konkrete indgange mod ét
  spørgsmål, etiketten kan sættes) — `afsaet` bruges også til de tre
  vurderingsdimensioner, der giver én karakter.
  **Sitet var ikke nede (3.11.)** — alle adresser svarede 200 herfra,
  certifikatet var gyldigt, og forsiden rendererede i Chromium. Det var
  brugerens eget netværk. Mål udefra, før du leder efter fejlen i repoet.

- **Sitet virkede ikke på en telefon (rettet 3.11.).** Brugeren sendte et
  skærmbillede af GeoGebra-siden, hvor de tre knapper i toppen lå oven i
  hinanden og løb ud over skærmkanten.
  **Årsagen var én manglende linje:** `.btn` havde ingen `display`, så et
  `<a class="btn">` blev `inline` — og en inline-kasses polstring fylder
  ikke lodret. Knapperne lå derfor oven på hinanden og stak 519 px ud på en
  390 px bred skærm. `.btn` er nu `inline-flex`, og i hero stables knapperne
  under 600 px.
  **Målingen afslørede en større fejl:** 22 af 43 sider scrollede sidelæns
  på en telefon. Altid brede tabeller — årsplaner, kildelister, tabeller i
  lektiearkene — plus én figur i en `.graphwrap`, der ikke kunne krympe
  (`flex:0 0 auto`). Alle 43 sider har nu
  `@media(max-width:600px){table{display:block;overflow-x:auto}}`, så en
  bred tabel ruller for sig selv i stedet for at trække i dokumentet.
  Vurderingstabellen på dansk-siderne er undtaget: den skal læses, ikke
  rulles, så den tvinges til `table-layout:fixed` og ombryder i stedet.
  **Mål det i en rigtig browser.** Playwright-opskriften er
  `newPage({viewport:{width:390,height:844}})` — ikke `viewportSize`, som
  bliver ignoreret, så man måler på 1280 og tror, alt er i orden.

- **Alle knapper gennemgået (3.11.).** Brugeren bad om at få rettet dem
  alle, så de virker. Et script måler nu hver knap på hver side ved 390 og
  1280 px og melder fire ting: overlap, noget uden for skærmen, knapper i
  samme række med forskellig top, og knapper under 40 px. Start: 2 overlap,
  22 ujævne og 22 for lave. Slut: **0 på alle fire, på begge bredder.**
  Fire rigtige fejl:
  1. `.btn` havde ingen `display` og blev `inline`. Rettet til `inline-flex`.
  2. Knapperne i hero var 44, 48 og 50 px høje og stod derfor 6-7 px
     forskudt. De har nu samme kasse: 48 px, `vertical-align:top`.
  3. Tapmål under 44 px på 22 sider. Hævet.
  4. Menuen i toppen brækkede over to linjer. Forsøgt løst med vandret
     rulning — men det **skjulte det sidste menupunkt**, og på GeoGebra-siden
     er netop det vejen tilbage til opgaverne. Rullet tilbage: menuen
     ombryder, men kompakt.
  **En CSS-regel kan tabe, selv om den står sidst.** `.jump{flex-wrap:nowrap}`
  virkede ikke, fordi originalen hedder `nav.jump` — element plus klasse
  vejer tungere end klasse alene. Den hedder nu `header.top .jump`.
  **Mål det, før du tror på det.** Målescriptet ligger i scratchpad og kan
  skrives igen fra beskrivelsen her: `newPage({viewport:{width:390,…}})` —
  ikke `viewportSize`, som bliver ignoreret.

- **Vercel-projekterne kortlagt (3.11.).** Det live site ligger på
  projektet **`kontiki-9klasse`** (`prj_WT1oGfW1ztnMBkYQ3tzH5Z4i1iup`) —
  det er det eneste, der har `mibelibsen.space` og `www.mibelibsen.space`.
  Alle andre har kun deres eget `.vercel.app`-navn.
  **Elleve projekter er rester** fra de fejlslagne deploy-forsøg: `kontiki`,
  `kontiki9`, `mibelibsen-site`, `mibelibsen-skole`, `mibelibsen-space`,
  `mibelibsen-9klasse`, `mibelib-space`, `matematik-9-klasse`,
  `matematik-9-kontiki`, `matematik-9-kontiki-probe` og
  `funktioner-og-ligninger-kontiki`.
  **Pas på navnene:** `mibelib-space` (den gamle dansk-side) og
  `mibelibsen-space` ligner hinanden, og ingen af dem er den live.
  **Reglen om ikke at bruge Vercels API holder kun halvt.** Læsning virker
  fint — projekter, domæner og deres id'er kan hentes. Det er *skrivning*,
  der ikke skal bruges, og **sletning kan slet ikke lade sig gøre**:
  `get_project_deletion_link` svarer `mutationExecuted: false` og
  `requires_user_action`. Vercel kræver, at et menneske bekræfter i
  dashboardet. Brug læsningen til at finde det rigtige id og give et
  præcist link — gæt aldrig på en projektadresse.

- **Klip ligningen fri (3.11.).** `materiale/klip-ligninger-fri.pdf`,
  bygget af `claude/byg_klip_ligninger.py`. Sjette ark, og det eneste, der
  ikke handler om geometri. Reglerne for at løse ligninger er lette at
  lære udenad og lige så lette at glemme, fordi de ikke ligner noget. På
  en vægt er de ikke regler: de er det eneste, man kan gøre.
  **A** 3x + 2 = 11 — fjern det samme fra begge sider, del resten i lige
  store bunker. **B** 5x + 1 = 2x + 7 — man må også fjerne x-brikker, ikke
  kun tal, og man behøver ikke vide, hvad de vejer. **C** 2(x + 3) = 14 —
  to ens bunker giver 2x + **6**; tretallet bliver ganget med.
  **x-brikken er 45 × 18 mm, og 45 går ikke op i 18.** Det er bevidst og
  vogtet af en assert: ellers kan svaret måles med en lineal i stedet for
  at regnes ud, og så er hele øvelsen spildt.
  **Antallet af brikker er regnet, ikke gættet.** Otte x-brikker og tyve
  1-brikker — lige præcis nok til den af de tre opgaver, der bruger flest
  (C bruger 6 + 14 = 20). En assert tjekker hver opgave mod arket.
  Vægten klippes ikke ud; den ligger på bordet, og brikkerne lægges oven
  på. Svararket viser de tre stillinger for hver opgave som små vægte med
  pile imellem — facit skal vise det, opgaven beder om.
  **Tre små figurer i hver sin ramme blev for bredt** (3 × 66 mm mod de
  184, der er plads til). De tegnes nu som ÉN figur med regnede afstande,
  og brikkerne i dem har ingen bogstaver — farven skiller dem ad, så
  figuren slipper for tekst i 2 punkt.
  **Navnet på flisen passede ikke længere**, og brugeren omdøbte den til
  **Matematik klip**. Ligninger er algebra, ikke geometri, men arket hører
  til: samme format, samme praksis.

- **Klip trigonometrien fri (3.11.).** `materiale/klip-trigonometri-fri.pdf`,
  bygget af `claude/byg_klip_trigonometri.py`. Femte ark, og det første
  uden en formel at klippe frem. I stedet en påstand, som saks og lineal
  kan afgøre: **forholdet mellem siderne afhænger kun af vinklen.**
  **A** fem trekanter — fire med 35°, én med 42°. De klippes ud, stakkes
  og måles; fire giver 0,574 i sidste søjle, den femte giver 0,669.
  **B** de samme målinger på 25°, 45° og 60°, sammenlignet med det
  lommeregneren kalder sin, cos og tan. Det er de samme tal. **C** en stor
  35°-trekant bliver et sigteinstrument: højde = øjenhøjde + 0,70 · afstand,
  og 0,70 er tallet, de selv målte i A.
  **Måleusikkerheden er regnet, ikke håbet.** Scriptet regner for hver
  trekant, hvad forholdet kan blive med ±0,5 mm på hver måling, og har
  tre asserts: de fires spand må ikke røre den falskes (ellers kan den
  ikke afsløres), det rigtige tal skal ligge i alle fire spand, og
  spandet skal blive smallere, jo større trekanten er. Det sidste er en
  pointe i sig selv og står som spørgsmål på arket: hvilken trekant gav
  det mest nøjagtige tal, og hvorfor?
  Trekanterne er drejet og spejlet, så de ikke ligner skalerede kopier —
  det er netop stakken, der skal afsløre, hvilke der hører sammen.
  Hyldepakningen regner selv, hvor de kan ligge, og vinkeltallet er lagt
  på vinkelhalveringslinjen uden for buen; et fast punkt inde i trekanten
  lagde 60°-tallet oven i buen.

- **Boksplot-siden (11.11.).** `boksplot.html`, bygget af
  `claude/byg_boksplot.py`, kort på `matematik.html`. Tre
  forklaringsafsnit og **20 spørgsmål med en figur til hvert**, delt i to
  quizzer: aflæsning (10) og forståelse (10).
  **Quizmotoren løftes ud af `statistik.html`** sammen med CSS'en og
  rammen omkring — overlay, navnefelt, fremgangslinje, resultattabel — så
  de to sider ikke kan komme til at opføre sig forskelligt. Kun
  `STORAGE_KEY` og modulnavnene byttes; ellers ville siderne dele gemte
  svar.
  **Alle tal regnes af rådataene** med den danske skolemetode, og
  metoden er prøvet af på et kendt eksempel, så den ikke kan skride
  ubemærket. Hvert spørgsmål har en assert på, at de tre svarmuligheder
  er forskellige, og sammenligningsspørgsmålene har asserts på selve
  pointen (at B *faktisk* har den højeste median, at kassen *faktisk* er
  smallest, at medianen ikke flytter sig, når den største værdi
  fordobles).
  **`figurer.py` fik `boksplot_par()`**: to boksplot på én fælles akse
  med jævne streger. Det er hele pointen — to boksplot tegnet på hver sin
  skala kan ikke sammenlignes.
  **Fejl fundet i browseren:** mine markeringer i talrækken hed
  `.tal.q`, og motoren tæller *alt* med klassen `q` som et spørgsmål.
  Siden troede, der var 22 spørgsmål. Klasserne hedder nu `kv` og `md`.
  Lær af det: når man låner en motor, arver man også dens selektorer.
  Prøvet igennem i Chromium: 20 besvaret, 20 af 20 rigtige, begge moduler
  10/10 i resultattabellen, forkert svar giver den rigtige rettelse, og
  intet vandret overløb.

- **Fyrtøjet som spil (11.11.).** `fyrtoejet.html`, også på
  **/fyrtoejet**. Hentet fra brugerens artefakt og sat op som en side:
  tre kamre med hver sin hund, et valg ved rebet (dræbe heksen som i
  eventyret, eller binde hende), galgebakken med fyrtøjet, og fem
  samtalespørgsmål til klassen til sidst.
  **Siden står for sig selv**, ligesom `algoritme.html`. Den er mørk, og
  sitets lyse sidehoved ville brække rummet, så der er kun en diskret vej
  hjem i spillets egne farver. Skrifterne hentes fra Google Fonts, men
  faldet tilbage til Georgia er bygget ind, så et webfilter ikke kan
  ødelægge den.
  **`tjek.py` fik en undtagelse mere.** Reglen om en figur på hver side
  leder efter `<svg>`, og hele spillet tegnes på et `<canvas>`. Begrundelsen
  står i listen, som den gør for `algoritme.html`. Spillet er prøvet
  igennem i Chromium: ingen JS-fejl, intet vandret overløb på 420 px, og
  hunden lader sig løfte.
  **Kort på forsiden (11.11.)** med mærkatet *Dansk*, lagt før de fire
  fagkort, så emnekortene bliver stående samlet.

- **Matematiske formler og fagord lagt op (11.11.).**
  `materiale/matematiske-formler-og-fagord-2017.pdf`, kort på
  `matematik.html`. Undervisningsministeriets opslagsbog til 7.-10.
  klasse og folkeskolens prøver, 2. udgave juni 2017. 74 sider, 2,9 MB,
  med tekstlag, så der kan søges i den.
  **Den afløste en forkert bog samme dag.** Først blev stx-formelsamlingen
  på A-niveau lagt op; jeg skrev på kortet, at den rækker ud over 9.
  klasse, og brugeren sendte den rigtige i stedet. Lær af det: slå op i
  PDF'ens forside, før den får et kort — titlen i filnavnet var
  «formelsamling», men niveauet stod kun på side 1.
  Kort på forsiden også, med mærkatet *Matematik*, ved siden af
  Fyrtøjet-kortet og før de fire fagkort.

- **Kalenderfil til FP9-prøverne (10.11.).**
  `vejledning/fp9-proever-januar-2027.ics`, bygget af
  `claude/byg_proevekalender.py`. Fem prøver, 18.–22. januar 2027,
  skrevet af fra et udtræk fra booking.testogprøver.dk.
  **Bookinglisten giver kun starttidspunktet.** Varighederne er slået op
  i UVM's retningslinjer, ikke husket: matematik 4 timer i alt (1 uden +
  3 med hjælpemidler, uden pause), dansk skriftlig fremstilling 3½ time,
  dansk læsning og retskrivning 1½ time (60 min retskrivning, så 30 min
  læsning). Kilden står i hver begivenheds beskrivelse, så den, der
  åbner kalenderen om to måneder, kan se, hvor tiderne kommer fra.
  **Outlook er kræsen med formatet:** CRLF, folding på 75 *oktetter* og
  ikke tegn, og tidszonen skrevet ind i filen som en VTIMEZONE, så
  tiderne ikke flytter sig. Foldningen bryder på tegngrænser, så et
  dansk bogstav ikke bliver hugget midt over. Scriptet har asserts på
  alle fire ting, og filen er efterprøvet med `icalendar`: fem
  begivenheder, alle 08:00 lokal tid, UTC+1 i januar.

- **Lektien om lineære funktioner flyttet til uge 44 (6.11.).** Første
  afsnit på arket hedder nu *«Svarer til opgave C og D, bare kun med tal,
  uden situation og eksempel.»* — brugerens egen formulering. Etiketten
  øverst siger **Uge 44 · 26.10 – 30.10**; ugens datoer er regnet med
  `date.fromisocalendar`, ikke slået op.
  Filnavnene med dato fulgte med: `lektieark/lektier-2026-10-26-…` og
  `facit/facit-lektier-2026-10-26-…`, så de passer til `tjek.py`'s
  mønster. **HTML-filen hedder stadig `lektier-uge41-funktioner-grafer.html`**
  — det er en offentlig adresse, der er linket fra matematiksiden, og den
  bliver ikke omdøbt for et ugenummer. Kortet og lektieplanen er rettet.

- **Facitlisterne er bygget om uden navnet (6.11.).** 18 PDF'er i
  `facit/` havde stadig «· Mibelibsen» i sidehovedet. `byg_facit.py` og
  `byg_facit_statistik.py` var allerede rettet, så de skulle bare køres
  igen. Indholdet er efterregnet ord for ord mod den gamle udgave af
  funktioner-facitten: identisk, kun sidehovedet er kortere. To gamle
  filer uden byggescript — `facit-statistik-hjemmeopgaver.pdf` og
  `facit-statistik-online.pdf` — har navnet endnu; de er to af de fire,
  `tjek.py` også brokker sig over navngivningen af.
  **Lektien om lineære funktioner var allerede udgivet** (uge 41, den
  6.10.). Siden svarer 200, kortet står på matematiksiden, og facitten
  svarer 404 på sitet, som den skal.

- **GeoGebra: hældningen forklaret ordentligt (4.11.).** Brugeren så det
  i klassen. To ting gik galt.
  **Ungerne rettede i den linje, der allerede stod i GeoGebra.** Trin 4
  beder dem skrive `-2x + y = 1` om til `y = 2x + 1`, og de troede, det
  skulle gøres *i programmet*. Så flyttede linjen sig. Der står nu en
  advarselsboks **som det første efter overskriften**: omskrivningen
  laves på papiret, og alt, hvad man skriver i GeoGebra, skrives på en
  **ny linje** i Input-feltet.
  **Hældningen var forklaret for hurtigt.** Trin 5 hed før «Få hældningen
  a» og sagde, at kommandoen tegner et trappetrin — uden at sige, hvordan
  man tegner et selv. Nu er der fire regnede figurer og fire tilfælde:
  ét trin (1 til højre, a op), fem trin (5 til højre, divider med 5 —
  præcis det, opgaven beder om), et trin **nedad** (negativ a, som i
  batteridelen af opgave C), og den anden vej rundt: **tegn linjen ud fra
  a og b**. Den sidste er pointen — hældningen er ikke et tal, man slår
  op, men en opskrift på at komme fra ét punkt på linjen til det næste.
  Figurerne bruger `figurer.py`'s `trappe`-parameter, der selv skriver
  «5 til højre» og «10 op» ud fra tallene.
  **Trin 8 om Rod fik samme behandling (5.11.).** Advarslen øverst:
  `Rod(f)` gør ingenting, fordi `f` er en *linje* og ikke en funktion —
  brug din egen `g`, og skriv på en ny linje. Derefter hvad et nulpunkt
  *er* (det x, der giver y = 0), hvordan man aflæser det på grafen, og
  hvordan man regner det ud i hånden i tre skridt, der bruger
  omskrivningen fra trin 4. To figurer: den stigende linje med nulpunkt i
  −0,5 og den faldende med nulpunkt i 4,5 — den sidste er batteridelen af
  opgave C. Til sidst: GeoGebra svarer med et *punkt*, men opgaven vil
  som regel kun have x-værdien, og den vil have en enhed på.
  Nulpunkterne regnes som `Fraction(-b, a)`, så −0,5 er eksakt, og en
  assert tjekker, at begge ligger inde i det tegnede vindue.

- **Navnet «Mibelibsen» er væk fra sitet (3.11.).** 64 forekomster på 39
  sider: sidehovedet («Mibelibsen · 9. klasse») og sidefoden. **Fjern
  betyder fjern** — der blev ikke sat et nyt navn ind, hverken domænets
  eller skolens. Sidehovedet hed først bare **9. klasse**; brugeren valgte
  bagefter **321flyv · 9. klasse**, sat i husets eget mønster med navnet i
  sort og resten i accentfarven, præcis som fagsiderne gør det
  («Matematik · Statistik»). De seks dybe matematiksider havde selv det
  mønster og hedder nu **321flyv · Statistik**, *· Manipulation*, *· Test
  i statistik* og så videre: navnet står der, og faget fremgår af
  spring-menuen nedenunder. Sidefoden slutter dér, hvor den stod før
  navnet: *Undervisningsmateriale · 9. klasse.*
  **De 24 byggescripts blev rettet med**, ellers ville navnet være kommet
  tilbage, næste gang en side blev bygget. Fire steder stod strengen delt
  over to linjer i Python og blev ikke fanget af den brede erstatning —
  de blev rettet hver for sig, efter at scriptet havde rapporteret dem.
  **Det, der IKKE blev rørt:** `mibelibsen/kontiki` (GitHub-repoet),
  `mibelibsens-projects` (Vercel-teamet) og projektnavnene i
  `claude/opsaetning.md`. De er adresser, ikke navne på sitet, og de ville
  gå i stykker.

- **mibelibsen.space viderestiller nu (3.11.).** 307 til 321flyv.com, sti
  for sti: `/matematik-klip.html` og `/u/anna` lander samme sted på det
  nye domæne. Svaret har `cache-control: max-age=0, must-revalidate`, så
  browseren gemmer den ikke — det var hele pointen med 307 frem for 308.
  Der ligger en påmindelse til 4.1.2027 om at fjerne domænet fra
  projektet.

- **Nyt domæne: 321flyv.com (3.11.).** Skolens webfilter blokerede
  `mibelibsen.space`. `.space` er en billig endelse, der bruges meget til
  spam, og mange filtre blokerer hele endelsen uden at se på indholdet.
  Domænet blev købt gennem Vercel og koblet på `kontiki-9klasse` — købt
  dér betyder, at DNS sættes op automatisk, så der skulle ingen poster
  ind nogen steder. `www` sender videre til apex med 308. Bagefter
  besluttede brugeren at bruge `mibelibsen.space` til noget andet, så
  hele sitet flyttede med.
  **Koden skulle næsten ikke rettes.** Alle sider linker relativt. Der var
  tre absolutte steder: viderestillingen `/u/eksempel` i `vercel.json`
  (nu relativ, og `byg_spoergeskema.py` skriver den også relativt, så den
  ikke kommer igen), `site` i `spoergeskema/opsaetning.json`, og `BASE` i
  `byg_sturmflut.py`. **En absolut adresse til sitets eget domæne er
  altid en fejl** — den virker, lige indtil domænet skifter, og så virker
  den i stilhed forkert.
  **En viderestilling redder ikke de printede QR-plakater.** De peger på
  `mibelibsen.space/u/<kode>`, og filteret blokerer forespørgslen, *før*
  viderestillingen bliver sendt. Skal de bruges igen, skal de printes
  forfra; scriptet laver dem med den nye adresse. Undersøgelsen var
  afsluttet, da domænet skiftede.
  **Overgangsperiode til 31.12.2026.** `mibelibsen.space` bliver på
  projektet som **307**-viderestilling til 321flyv.com, så gamle links
  virker året ud. 307 og ikke 308 med vilje: en permanent viderestilling
  bliver cachet hårdt i browseren, og så kan domænet ikke genbruges
  bagefter uden at genere alle, der har besøgt det. Efter nytår fjernes de
  to adresser fra `kontiki-9klasse`.

- **Matematik klip — én flise (3.11.).** `matematik-klip.html`, bygget af
  `claude/byg_matematik_klip.py`, linket fra `matematik.html`. Hed først
  **Geometri klip**; da ligningsarket kom til, passede navnet ikke
  længere, og brugeren valgte **Matematik klip**. Den gamle adresse
  `/geometri-klip.html` sender videre i `vercel.json`, så et delt link
  ikke går i stykker. De fire
  klippeark fyldte fire kort på matematiksiden; nu er der ét kort,
  **Geometri klip**, og en side bagved med dem alle.
  **Miniaturerne er de rigtige figurer.** Scriptet importerer de fire
  byggescripts og henter figuren derfra — mm-målene i `<svg>`-taggen
  fjernes, så den kan skalere på en skærm, men `viewBox` bliver stående.
  Ændrer et ark sig, ændrer billedet sig med; de kan ikke komme til at
  vise hver sit. Siden har også den praktiske besked, der manglede alle
  fire steder: **print i 100 %, ikke «tilpas til side»**.
  Knapperne hedder `.btnlink` på matematiksiden, ikke `.btn` — CSS'en
  arves derfra, så klassenavnet skal passe til kilden.

- **Klip Pythagoras fri (3.11.).** `materiale/klip-pythagoras-fri.pdf`,
  bygget af `claude/byg_klip_pythagoras.py`. Fjerde ark. Her er saksen
  ikke bare et greb, den er den eneste udvej: **kvadratet på den lange
  side ligger skævt og kan ikke tælles.**
  **A** tre kvadrater på en 3-4-5-trekant — 9 og 16 kan tælles, det skrå
  skal klippes ud og lægges på ternkvadratet: 25. **B** fire ens trekanter
  i en (a+b)-ramme, lagt på to måder: samme ramme, samme trekanter, altså
  lige store huller — 3×3 + 4×4 i den ene, 5×5 i den anden. **Det er
  beviset**, og det bruger ingen steder, at siderne er 3, 4 og 5. **C**
  Perigals opdeling: fire stykker af 4×4-kvadratet plus 3×3-kvadratet
  fylder 5×5-kvadratet præcis.
  **Perigal er regnet efter, ikke tegnet.** Snittene går gennem midten,
  parallelt med og vinkelret på den lange side; enderne lander præcis på
  kanten, fordi hver halvdel er c/2 lang. Og arealer, der stemmer, er ikke
  nok — brikkerne kunne overlappe. Scriptet lægger derfor de fem stykker
  på plads og tjekker 14 400 punkter: hvert punkt skal være dækket præcis
  én gang. Gør det ikke det, bliver arket ikke bygget.
  Svararket viser begge opstillinger i rammen og de fem stykker på plads —
  facit skal vise det, opgaven beder om.
  **Mellemrum mellem to inline-block'e tæller med i bredden.** Rammen og
  trekanterne var 179 mm tilsammen og burde kunne stå side om side på de
  184 mm, men mellemrummet i HTML'en skubbede dem fra hinanden, så de
  havnede på hver sin side. `.rad{font-size:0}` løste det.

- **Klip overfladen fri (3.11.).** `materiale/klip-overfladen-fri.pdf`,
  bygget af `claude/byg_klip_overflade.py`, linket fra `matematik.html`.
  Tredje ark i rækken. Her er saksen ikke et hjælpemiddel, den er hele
  pointen: **overfladen er præcis det, der ligger fladt, når legemet
  klippes op.** Et legeme har ikke en overflade, man kan måle på; en
  udfoldning har et areal, man kan måle. **A** kassen (seks flader, tre
  par, 128 cm²), **B** cylinderen (88,0 cm²), **C** pyramiden (70,8 cm²).
  **Cylinderen er den vigtigste.** At den krumme side er et rektangel, og
  at dets bredde *er* omkredsen, kan ikke ses — kun vises. Derfor har
  rektanglet en limflap, så det kan rulles til et rør, og cirklen prøves af
  i åbningen. Rektanglets bredde er 125,7 mm, og 2 · π · 20 er det samme
  tal; det er ikke et tilfælde, og det er det, de selv skal opdage.
  **Kassen og pyramiden er de samme legemer som på rumfangsarket**, og
  målene hentes med `importlib` fra `byg_klip_rumfang.py`, så de to ark
  ikke kan komme til at sige hver sit. Klippearket indeholder derfor kun
  cylinderen, med en boks øverst om at finde de to andre frem og klippe dem
  op igen. Det holdt arket på tre sider i stedet for fem.
  **Sidehøjden mod den korte side er præcis 50 mm** — en 3-4-5-trekant — og
  en assert vogter det. Fælden er, at de regner trekanternes areal med
  pyramidens højde i stedet for trekantens egen; den står i svararket.
  **Decimalkomma.** Alle tre klippeark fik en `kom()`-funktion, så facit
  skriver 70,8 cm² og ikke 70.8 — dansk notation, også i de ark der kun
  læses af en voksen. De to ældre ark blev bygget om samtidig.

- **Klip rumfanget fri (3.11.).** `materiale/klip-rumfanget-fri.pdf`,
  bygget af `claude/byg_klip_rumfang.py`, linket fra `matematik.html`.
  Efterfølgeren til arealarket, samme greb: **A** grundfladen som
  centimetertern (24 cm²), **B** kassens udfoldning (6 × 4 × 4 cm = 96 cm³,
  fire lag), **C** pyramiden med *samme* grundflade og højde — den fylder
  præcis en tredjedel, 32 cm³.
  **Tredjedelen er hele pointen.** Rumfanget af en kasse kan forklares;
  tredjedelen kan ikke på dette trin. Den kan kun vises, og den vises ved
  at hælde. Derfor skal der ris eller sand på bordet.
  **Limflapperne regnes, ikke tegnes på øjemål:** `_flap()` finder den
  udadvendte normal ud af trekantens tredje hjørne, så en flap på en skrå
  kant vender rigtigt. Og **rammen om figuren regnes af de punkter, den
  faktisk bruger** — et gæt gav et pyramidenet på 206 mm, og A4 har 184.
  `svg()` har nu en assert på begge mål.
  **Kassen blev sænket fra 5 til 4 cm**, fordi nettet ellers ikke kunne dele
  side med grundfladen, og arket blev fem sider med en næsten tom
  førsteside. Tallene er stadig eksakte: 96 / 3 = 32.

- **Intro til GeoGebra, skrevet om med skærmbilleder (3.11.).**
  `geogebra-lineaere-funktioner.html`, bygget af `claude/byg_geogebra.py`.
  Hed før «GeoGebra på ti minutter»; brugeren bad om bare **Intro til
  GeoGebra**.
  **Jeg tog fejl to gange om trin 1.** Først skrev jeg «vælg Graf» af
  hukommelsen. Så målte jeg efter og skrev, at man ikke skal vælge noget —
  men jeg målte på et *andet* besøg. **Ved første besøg kommer app-listen
  frem af sig selv**, og dér skal man vælge Graf. Brugeren havde ret begge
  gange. Lær af det: når noget afhænger af, om det er første besøg, skal
  der måles i en frisk browserkontekst, ikke i den, der allerede har klikket.
  **Elleve skærmbilleder, hentet fra den rigtige app.** `claude/
  hent_geogebra_billeder.mjs` åbner geogebra.org/classic i Chromium på
  dansk, bygger hver tilstand med appens eget `ggbApplet`-API og
  fotograferer vinduet; `claude/beskaer_geogebra_billeder.py` beskærer
  værktøjslinjen væk og komprimerer. **Billederne må ikke tegnes i
  hånden** — så holder de op med at ligne det, ungen ser. Ændrer GeoGebra
  udseende, køres de to scripts igen. 213 kB i alt for elleve billeder.
  **Kvantisering kan spise farver.** `quantize` med 96 farver og MEDIANCUT
  gjorde de blå punkter og den orange trappe grå. FASTOCTREE med 256
  farver holder på de få mættede farver og giver næsten samme filstørrelse.
  Og: beskæringen blev lavet *på stedet*, så de oprindelige filer var væk,
  da fejlen blev opdaget — billederne måtte hentes forfra.
  **API'et taler engelsk, algebravinduet dansk.** `evalCommand('Line(A,B)')`
  virker; `Linje(A,B)` gør ikke. Men algebravinduet skriver `Linje(A, B)`
  og `Hældning(f)`, så de danske navne på siden er bekræftet af
  skærmbillederne selv.
  **Trin 4 er nyt og handler kun om omskrivningen.** GeoGebra skriver
  `-2x + y = 1`; den gamle side sagde bare «flyt leddet over» og gik
  videre. Nu er det tre nummererede skridt, en huskeregel og en tegning,
  hvor leddet flytter over med en pil og skifter fortegn. Figurens
  koordinater er regnet: i en monospace-skrift er et tegn 0,6 gange
  skriftstørrelsen bredt, så rammen om leddet kan lægges præcist.
  **Trin 5 siger nu, hvad kommandoen hedder.** Før stod der «det her er
  den vigtigste kommando på siden» uden at nævne den. Den hedder
  **Hældning**, og grunden står der nu: den tegner trappetrinnet, så tallet
  kan ses, ikke bare læses.
  **Punkt for punkt.** Ny sektion med ti afkrydsningspunkter — ét
  håndgreb hvert. Det tiende er det vigtigste: *arbejd videre med den
  funktion, du nu har lavet.* Den er værktøjet, ikke målet.

- **Klip arealet fri (3.11.).** `materiale/klip-arealet-fri.pdf`, bygget af
  `claude/byg_klip_areal.py`, linket fra `matematik.html`. Tre arealformler,
  som ungerne klipper sig frem til: parallelogram → rektangel, to trekanter →
  parallelogram, cirkel i 16 udsnit → næsten-rektangel. **Formlerne står
  ikke på arket.** Uden saks kan ingen af delene lade sig gøre.
  **Figurerne er i millimeter, ikke pixels** — de skal printes i rigtig
  størrelse, for der måles på papiret bagefter: parallelogram 80 × 50 mm,
  trekant 70 × 40 mm, cirkel r = 40 mm. Derfor ligger de i byggescriptet og
  ikke i `figurer.py`, som tegner til skærm. Scriptet har en assert på, at
  halv omkreds · radius giver præcis cirklens areal; holder den ikke, er
  øvelsens pointe forkert, og arket bliver ikke bygget.
  **Niveauet nævnes ingen steder.** Brugeren bad udtrykkeligt om, at der
  ikke står klassetrin — hverken på arket eller på kortet.
  Svararket ligger i `vejledning/` og er ikke i git. Det har også de to
  ting, der driller: at højden ikke er den skrå side, og spørgsmålet om,
  hvad der sker ved 32 eller 64 udsnit — grænseovergangen, som kan mærkes
  med en saks, længe før den kan skrives.

- **Svarene fra Hamborg delt i fem segmenter (3.11.).**
  `claude/byg_hamborg_segmenter.py` henter de 170 besvarelser fra
  regnearket og bygger `tekster/hamborg-segmenter.docx` og `.pdf` — ét
  segment til hver gruppe: byen og at rejse væk, skole og job, fritid og
  venner, mobil og medier, mad og værdier.
  **Segmenterne er afbalanceret efter målt arbejde**, ikke efter fornemmelse:
  352, 299, 208, 211 og 304 *forskellige* svar at oversætte. Første
  opdeling gav segment 5 over 400, og spørgsmålet om rejser flyttede derfor
  til segment 1.
  **Frie svar står én gang med antal** — `Hafen (12)` — ikke 170 gange.
  Grupperne oversætter hvert svar én gang og kan se, hvad der er typisk.
  **82 af de 170 bor ikke i Hamborg.** Derfor står der *keine Ahnung, bin
  nicht von hier* i en del af svarene om byen. Det står som en advarsel
  øverst i dokumentet: det er et resultat, ikke en fejl i skemaet.
  **Hverken data eller dokumenter er i git** — det er besvarelser fra unge
  på en anden skole, og repoet er offentligt. Scriptet er kilden.

- **Rettighedsbeskyttede tekster i det offentlige repo (3.11.).**
  `tekster/digital-dannelse-faktalink.pdf`, `tekster/big-tech-debatindlaeg-politiken.pdf`
  og `tekster/alkoholpolitik-guide.pdf` er udelukket fra *sitet*, men
  GitHub-repoet er offentligt, så de kan hentes derfra. En skoleaftale
  dækker deling med klassen, ikke udgivelse på GitHub.
  **Brugeren er gjort opmærksom på det 3.11. og har besluttet, at de bliver
  liggende for nu.** Rejs det ikke igen af dig selv. At fjerne dem helt
  kræver en omskrivning af historikken.

- **Tysk: resultatsiden taget ned igen, opgavesiden sat op (3.11.).**
  `tysk-resultater.html` blev bygget og udgivet om formiddagen og **slettet
  igen samme dag** — brugeren ville have den som PDF i hånden i stedet, og
  sitet skal i stedet bære selve opgaven. PDF'en er sendt. Scriptet
  `claude/byg_tysk_resultater.py` ligger der stadig; kør det, hvis siden
  skal op igen.
  `tysk-segmenter.html`, bygget af `claude/byg_tysk_segmentopgave.py`,
  er gruppeopgaven: fem segmenter, fem grupper, hvad de skal oversætte og
  sammenfatte, og hvad de afleverer. Start **tirsdag 10. november**, så
  Peter og Peter kan tage fat.
  **Segmenterne importeres fra `byg_hamborg_segmenter.py`** — side og
  dokument kan ikke komme til at sige hver sit. Figuren viser, hvor meget
  hver gruppe skal oversætte, fordi det første spørgsmål fra en gruppe
  altid er, om de har fået mere end de andre.
  **Dokumentet med de 170 besvarelser ligger ikke på sitet og linkes ikke
  derfra.** Brugeren blev spurgt 3.11. og valgte, at hun selv sender filen
  til lærerne. Siden siger, at dokumentet fås af læreren.

- **Dybe links kun når de skal bruges (afgjort 20.10.).** Reglen i
  CLAUDE.md gælder, når brugeren skal **gøre** noget i en grænseflade —
  Vercel-indstillinger, GitHub, et kontrolpanel. Den gælder ikke, når et svar
  bare fortæller, at en side er lagt op: der er mibelibsen.space-adressen
  støj. Skriv filnavnet i stedet.
- **Repoet er offentligt, og ungernes fornavne ligger i det** —
  `spoergeskema/unger.txt`, `unger-links.tsv`, QR-plakaterne og
  `/u/<navn>`-redirects i `vercel.json`, committet 22.9.
  **Afgjort 7.10.: det er i orden.** Kun fornavne, ingen følsomme oplysninger.
  Spørg ikke om det igen.
- **Bordplanen ligger i `spoergeskema/bindinger.json`** — både bindingerne
  (hvem der skal sidde sammen, og hvem der ikke må) og under `fast` selve
  planen, bord for bord. Den er i git med vilje: sidst lå det, at Johan og
  Silke er tvillinger, i en samtale og ikke i repoet, og så var det væk.
  Mappen er udelukket i `.vercelignore`, så filen ikke kommer på sitet.
  Selve PDF'erne er ikke i git — de bygges af scriptet og sendes i Code.
  Begge er ignoreret; `bordkort-*.pdf` blev glemt i mønstret 7.10. og er
  taget ud igen.
- **Scriptet laver to filer:** `bordplan-<dato>.pdf` med oversigten og den
  alfabetiske liste, og `bordkort-<dato>.pdf` med ét A4-ark pr. bord til at
  lægge på bordene. På bordkortene står navnene på den side, der vender væk
  fra tavlen, **på hovedet** — arket ligger fladt, så hver unge læser sit
  eget navn rigtigt vej fra sin egen plads. En pil viser, hvilken kant der
  skal vende mod tavlen.
- **Ny bordplan (7.10.).** Lokalet har **fem gruppeborde**, ikke dobbeltborde —
  den første udgave gættede på 12 og er slettet. 23 unger fordeles jævnt som
  5+5+5+4+4, tre borde forrest og to bagerst, med tavlen foran. Bindingen
  *Emilie ved siden af Anna* er holdt, men **ikke markeret på arket** —
  den er en regel for, hvem der sidder hvor, og ikke noget ungerne skal
  kunne læse ud af bordplanen. Scriptet siger i terminalen, at den holder.
  Bygges af
  `claude/byg_bordplan.py` med en fast frø, så den samme plan kan laves igen;
  scriptet nægter at skrive filen, hvis en binding ikke er overholdt, hvis en
  unge er blevet væk, eller hvis bordene bliver for smalle.
  **PDF'en ligger i `vejledning/`, som er udelukket fra deploy** — den
  indeholder ungernes navne og må ikke på sitet.
- **Planen er nu en kilde (7.10.).** Bordene er ikke lige store:
  **bord 1 har syv pladser, de fire andre har fire** — 23 stole til 23 unger,
  og det går lige op. Tallene står under **`pladser`** i `bindinger.json`.
  Sidder der flere ved et bord, end der er stole til, siger scriptet det både
  i terminalen og med rødt nederst på oversigten, så det ikke skal opdages,
  når ungerne står i lokalet.
  **Én skriftstørrelse på hele arket.** Regnes navnene hver for sig, bliver
  *Nor* dobbelt så stor som *Helene* ved samme bord; regnes de pr. bord,
  står bord 3 mindre end bord 2, fordi *Caroline* er lang. Begge dele ser
  ud, som om forskellen betyder noget.
- **Lokalet står i `LOKALE` i scriptet (7.10.).** Rækkerne er væk; hvert bord
  har en retning og en plads ved en væg:

  ```
  +-------------------- T A V L E --------------------+
  |                                            [2]    |
  | []                  | 1 |                  | |    |
  | dør     | 4 |       |   |                         |
  |         |   |       (for enden)                   |
  | []                                         [3]    |
  | dør                                        | |    |
  |                     [  5  ]                       |
  +---------------------------------------------------+
  ```

  **Planen er tegnet SET FRA TAVLEN, og det vender arket om.** Står man ved
  tavlen og ser ind i lokalet, har man højre væg på sin højre hånd — men på
  et kort med tavlen øverst ligger den væg i arkets **venstre** side. Første
  udgave 7.10. var spejlvendt, fordi jeg tegnede det, som man ser rummet
  bagfra. Alt hvad der hedder venstre og højre i `LOKALE` og i `bindinger.json`
  er set fra tavlen, ikke fra arket: de første pladser ved et bord er den
  **højre** langside og tegnes i arkets venstre kant.

  **Lokalet er ca. 6 m bredt og 8 m dybt** — dybere end bredt. Derfor står
  oversigten på **højkant**; på tværs blev rummet tegnet bredere end dybt, og
  så lignede planen ikke det lokale, den handler om. Målene står i
  `RUM_BREDDE_M` og `RUM_DYBDE_M`, og målestokken (1:32) følger af dem.
  Bordkortene er stadig på tværs.
  **Bord 1 står på langs** midt i lokalet med kortenden væk fra tavlen: tre på
  hver langside og én for enden. Den plads er **Milius'**. I `fast` er bord 1's
  rækkefølge derfor tre til venstre set fra tavlen, tre til højre, og den
  sidste for enden. Bord 2 og 3 står ved venstre væg, bord 4 ved højre væg
  mellem de to døre, bord 5 ved bagvæggen.
  **Navneskiltene er bredere end en stol**, ellers kan navnene ikke stå der.
  Det går ud over gangene mellem bordene, så scriptet nægter at tegne, hvis
  der bliver under 30 cm imellem — ungerne skal kunne komme hen til pladsen.
  Det står i foden, at skiltene er større end en stol.
  **Scriptet tjekker også, at to borde ikke står oven i hinanden.** En
  tegning, der er regnet forkert ud, er ikke til at se på.
  **`naboer()` regner ud, hvem der faktisk sidder ved siden af hvem** — på
  samme langside, og pladsen for enden rører den bageste på begge sider.
  Over for hinanden tæller ikke. Det er den, `sammen` tjekkes med, så
  *Emilie ved siden af Anna* betyder det, der står.
  **De fire borde, der står på langs, får bordkort på langs:** tavlen peger
  mod arkets venstre kant, ikke opad. På bord 1 står pladsen for enden ude i
  højre side drejet en kvart omgang — den vej, Milius sidder. Kun bord 5 ved
  bagvæggen har kortet med tavlen opad.
- **Ramme til ungernes egen stand om plastik (20.10.):**
  `plastik-stand.html`, bygget af `claude/byg_plastikstand.py`. Feature uge
  44: grupper på 3-5 laver deres eget korte forløb og holder det fra en
  stand for besøgende fra andre klasser og forældre.
  Siden er **rammen, ikke forløbet**: fem dele (mål, standen, medie- og
  materialeliste, opgaveliste, roller og ansvar), og hver del har en
  forklaring og et tomt felt — linjer eller et skema med kolonner. Printer
  en gruppe siden, har de deres plan på ét ark, der kan ligge på standen.
  **Der er ingen eksempler på siden, og det er med vilje (afgjort 20.10.).**
  Første udgave havde et gennemført eksempel på hver del. Det opfinder
  undervisningen for ungerne: et eksempel bliver skrevet af i stedet for
  tænkt. Målfiguren giver sætningsstarter, ikke svar.
  **Siden linker heller ikke til værkstedssiden.** Inspirationen skal komme
  fra ungernes egne noter fra naturfagsugen.
  **Standen har ingen zoner og intet flow (afgjort 21.10.).** Jeg havde
  tegnet en `standplan` med zoner i en rækkefølge og den besøgendes vej
  igennem. Sådan er standen ikke. Figuren er væk — også ud af
  `figurer.py` — og i stedet er der en ternet tegneflade med linjer under:
  *tegn den, og beskriv den*. Ungerne skal beskrive standen, ikke flowet
  omkring den.
  **Dagene:** åbent både **fredag og lørdag**, ca. **15 minutter** pr.
  besøgende. Tallet står tre steder — rammen, prøvekørslen og tjeklisten —
  og de skal følges ad.
  De hårde rammer står først: ét bord, 7-10 minutter pr. besøgende, skal
  kunne køre hele dagen, og **besøgende er både børn og voksne** — samme
  stand skal virke for en fra 3. klasse og for en forælder.
  **Tiderne i ugeplanen er et eksempel, ikke skemaet.** Det står i
  figurteksten, så ungerne ikke tager mandag-fredag for pålydende.
  Ny figur i `figurer.py`: `standplan` — bordet set oppefra med zoner, hvem
  der står hvor, og den rute den besøgende går.
- **Fagtekst om socialisering (20.10.):** `hvad-er-socialisering.html`,
  bygget af `claude/byg_socialisering_tekst.py`. Den findes, fordi der ikke
  var nogen: det frie danske materiale er enten leksikonkort (lex.dk) eller
  skrevet til gymnasiet (samfundsfag.dk, Levende Grønland) — resten ligger
  bag betaling hos Clio, Gyldendal og Alinea. Fem afsnit med fire figurer:
  arenaerne som ringe, norm → brud → sanktion, krydspres, og algoritmens
  kredsløb. Slutter med fem spørgsmål, der kan stilles til ungernes egne
  svar i uge 43, og en kildeliste. Ligger på `samfundsfag-tekster.html` som
  åben for alle, og er linket fra `kvalitativ-analyse.html`.
  Tre nye figurer i `claude/figurer.py`: `socialisationsringe`, `krydspres`
  og `kredsloeb`. De regner alle skriftstørrelsen ud af pladsen — ringene
  måler korden dér, hvor teksten når længst ud, ikke på midterlinjen, for
  ellers løber den yderste tekst ud over kanten med et par bogstaver.
- **Pecha Kucha (20.10.):** siden `pecha-kucha.html` til ungerne, bygget af
  `claude/byg_pecha_kucha_side.py`, og skabelonen
  `materiale/pecha-kucha-skabelon.pptx`, bygget af
  `claude/byg_pecha_kucha.py` + `.mjs`. 20 tomme slides, hver sat til at
  skifte efter 20 sekunder. pptxgenjs kan hverken skrive slideovergange
  eller en rigtig billedpladsholder, så scriptet retter begge dele bagefter
  i OOXML'en. Manuskriptet skrives i noterne, hvor hvert slide har et
  ordantal.
  **Skabelonen ligger i `materiale/` og ER i git** — i modsætning til
  bordplanen. Reglen om, at byggede filer ikke hører i versionsstyringen,
  viger for en anden: det, der udgives, skal ligge i git, ellers kan Vercel
  ikke servere det. Ungerne henter den fra siden.
  Ny figur i `figurer.py`: `slidebaand` — de 20 slides som lige brede
  felter, eventuelt farvet op efter hvem der taler.
  **pptxgenjs ligger ikke i containeren** — `npm install -g pptxgenjs`, og
  den importeres med sin fulde sti, fordi et ES-modul ikke kan slå globale
  pakker op på navnet. Den validerende `validate.py` fra pptx-skillen skal
  køres med `python3.13`, ikke `python3`: modulerne ligger i 3.13.
- **Faktalinks *Digital dannelse* er lagt på tekstsiden (20.10.).** PDF'en
  ligger i `tekster/`, som er udelukket fra deploy, og kortet linker til
  klassens Teams. Rettighederne er dækket af skolens aftale, og en
  skoleaftale giver ret til at dele med klassen på en lukket platform — ikke
  til at lægge teksten frit på sitet. **Teksten er fra januar 2016, og dens
  tal er fra 2013-2014.** Det står på kortet: brug den til begreberne og
  `digital-socialisering.html` til tallene.
- **Årsplanen for samfundsfag er rettet.** Uge 43 er skilt ud som sit eget
  forløb, *Digital socialisering: kvalitativ analyse*, og kriminalitet og
  overvågning rykker til uge 44–47. Antallet af uger pr. tema er uændret.
- **Samfundsfag har nu sit eget regneark.** Der fandtes kun ét til matematik.
  `aarsplan-samfundsfag-2026-27.xlsx` bygges nu af samme script som siden, med
  samme opbygning som matematikkens, og siden har fået en hent-knap.
- **`tjek.py` sammenligner nu begge årsplaner med deres regneark.** Ugefeltet
  står som "33" i matematikplanen og som "32 - 39" i samfundsfagsplanen, så
  kontrollen leder efter de mærkater, siden selv bruger, i stedet for kun rene
  tal.
- **`kvalitativ-analyse.html` er bygget — oplæg til uge 43.** Metoden i fem
  trin med procesdiagram, et gennemført eksempel hvor fem opdigtede svar kodes
  og kategoriseres, gruppeopgaven, fire fælder og en ordliste. Bygges af
  `claude/byg_kvalitativ.py`.
  **Eksempelsvarene er opdigtede og mærket som det** — ungernes egne svar må
  ikke ligge på sitet.
- **Afsnittet "Jeres egne tal" er slået fra igen (6.10.).** Ungerne nåede ikke
  at oversætte spørgeskemaerne færdigt, og svarene viste sig ikke at være
  sammenlignelige på tværs af de to sprog — besvarelserne bruges kvalitativt i
  stedet. Koden er bevaret bag flaget `VIS_EGNE_TAL` i
  `claude/byg_digital_socialisering.py`, så afsnittet kan komme tilbage uden at
  skulle skrives igen.
- **Figuren lagde op til en misforståelse, og brugeren fangede den.** Søjlen
  "Alle over 15 år" på 16 % stod ved siden af 27 % og 28 % for de unge og lignede
  en tredje aldersgruppe — så så det ud, som om helheden var mindre end delene.
  Den er nu grå, hedder "Hele befolkningen", og siden har fået en boks, der
  svarer på spørgsmålet: **et gennemsnit er ikke en sum, og det kan ligge under
  hver eneste gruppe, man kan se i figuren.** `figurer.soejler()` kan nu farve
  hver søjle for sig, netop så en referencesøjle kan skilles ud.
- **Lære: tjek linket, før det kommer på sitet.** Et link, der ser rigtigt ud i
  et søgeresultat, er ikke et link, der virker.

---

## Rettet 6. oktober 2026 · hverdagseksempler

- **Hver illustration på funktionssiden har fået et hverdagseksempel efter sig.**
  Syv stykker: taxaens pris, vand i en balje, elregningen, kontoen der bliver
  tom, to fitnesscentre, opsparing til en telefon og euro vekslet til kroner.
  Hvert eksempel har rigtige tal, en udregning der kan følges skridt for skridt,
  og sin egen graf med rigtige enheder på akserne.
- **Hverdagstal hører kun til sitet**, aftalt 6. oktober. Lektiearkene bliver
  ved med at være rene tal, så ungerne træner regnereglen uden at skulle tyde en
  situation først.
- **Uge 39-lektien er også udgivet 6. oktober.** Arket er helt og holdent om
  ligninger — der var intet fremmed emne at tage ud, som der var i uge 41. Kun
  sproget er rettet: indledningen siger nu, at opgaverne er rene tal uden en
  situation, der først skal tydes, og facit bruger samme ord som arket
  ("regneprogram", ikke "CAS"). Ugen 21.09–25.09 er passeret; den voksne
  besluttede at udgive alligevel.
- **Uge 41-lektien er udgivet 6. oktober** og ligger nu i roden med et kort på
  `matematik.html`. Arket handler kun om lineære funktioner: ligningsløsningen
  er taget ud (opgave B's "vis ved regning, at skæringspunktet er rigtigt"), og
  de to steder, hvor nulpunktet skulle tjekkes ved regning, aflæses nu på
  grafen. **Nulpunkterne står ved magt** — de hører til lineære funktioner.
  Facit er bygget om med.
- **Opgave C og D på sitet er lavet om til hverdagsopgaver.** Opgave C er nu
  en kajakudlejning (to kvitteringer), et telefonbatteri (nulpunktet er det
  klokkeslæt, telefonen dør) og en sammenligning af to telefoner, der ændrer sig
  hver sin vej. Opgave D er to mobilabonnementer, hvor skæringspunktet er
  grænsen, hvor det bedste valg skifter. Samme færdigheder, samme antal
  delspørgsmål, og begge facitlister er bygget om med.
- **Tallene er valgt, så de ligger på gitterlinjerne.** Ellers er en
  aflæsningsopgave gætteri: b = 50 og 150 kr, skæringen i (10, 250), batteriet
  80 % og 50 %. Trappetrinnet i opgave D går 5 GB, fordi 1 GB er mindre end én
  gitterlinje.
- **`koordinatsystem()` har fået `aksenavne`**, så en graf kan sige kWh og kr i
  stedet for x og y.
- **En unge fangede en fejl i baljen.** Eksemplet sagde 9 liter efter 2 minutter
  og 34 efter 7, hvilket giver `y = 5x − 1` — altså minus én liter i baljen, før
  hanen blev åbnet. Tallene er rettet til 14 og 39, så b bliver 4 liter, og
  eksemplet forklarer nu selv, hvorfor grafen ikke starter i (0, 0).
  **Lære: når en hverdagsgraf har en enhed, skal b også kunne lade sig gøre i
  virkeligheden.** Det er ikke nok, at hældningen passer.
- **`tjek.py` kender nu forskel på en abstrakt og en virkelig graf.** En graf,
  hvis akser hedder x og y, skal have kvadratiske tern. En graf med rigtige
  enheder på akserne kan ikke have samme skala og springes over.

---

## Rettet 6. oktober 2026

- **Håndtegnet graf fundet og rettet.** Figuren til `y = 2x + 1` på
  `funktioner-og-ligninger.html` var tegnet på øjemål: linjen havde hældning
  **6/5 i stedet for 2**, det blå punkt lå i **(2, 4)** hvor forskriften giver
  **(2, 5)** — derfor svævede det ved siden af linjen — og akserne havde ingen
  tal. Figuren er bygget om med `figurer.koordinatsystem()`, så alle
  koordinater beregnes, og efterregnet bagefter ved at læse pixelkoordinaterne
  ud af den færdige SVG og omregne dem til grafkoordinater.
- **`koordinatsystem()` har fået `trappe=(a, b, x0)`**, som tegner trappetrinnet
  "1 til højre og a op". Hældningen er den definition, teksten bruger, og den
  skal vises, ikke kun stå. Funktionen fejler, hvis trinnet falder uden for
  koordinatsystemet.
- **Akserne havde ikke ens skala — i nogen af graferne.** Det var den
  egentlige fejl: en x-enhed fyldte op til 68 px og en y-enhed kun 25 px, så
  en linje med a = 2 så knap tre gange for stejl. Alle seks koordinatsystemer
  på `funktioner-og-ligninger.html` og i uge 41-lektien er bygget om med
  kvadratiske tern. Linjer og punkter er uændrede, så alle svar er de samme —
  kun aksernes områder er valgt, så x-spændet og y-spændet er lige store.
- **`koordinatsystem()` har fået `ens=True` som standard.** Figuren beregner nu
  sin egen højde ud fra skalaen og fejler, hvis de to områder er mere end tre
  gange forskellige. Akser med hver sin enhed — kroner mod antal — skal sætte
  `ens=False`; der betyder 1:1 ingenting.
- **`tjek.py` måler nu skalaen** på hver graf på sitet og giver FEJL, hvis de to
  akser ikke har samme antal pixels pr. enhed. Den fangede med det samme to
  grafer mere i uge 41-lektien, som jeg ellers havde overset. Lektiearkets PDF
  i `lektieark/` er bygget om.
- **Facitlisterne er skrevet om som kode.** De syv facitlister til forløbet
  fandtes kun som færdige PDF'er, så deres skæve figurer kunne ikke rettes —
  de måtte skrives først. `claude/byg_facit.py` holder nu indhold, figurer og
  efterregning, og bygger alle syv. Hvert svar kontrolleres ved at sætte det
  ind i ligningen, før filen skrives. De to grafer med kroner på y-aksen
  beholder deres egen skala (`ens=False`) — der betyder 1:1 ingenting, og det
  står nu i figurteksten.
- **Et lektieark kom ud i Letter i stedet for A4.** `@page` manglede `size`,
  og så vælger Chromium Letter. Tretten sider manglede det. `tjek.py` giver nu
  FEJL for en printbar side uden `size:A4`.
- **De øvrige elleve facitlister er også skrevet om.** Statistik modul 1–4,
  manipulation modul 1–3 og lektierne i uge 33 til 36 bygges nu af
  `claude/byg_facit_statistik.py`. Skabelonen er flyttet ud i `claude/facit.py`,
  så de to byggescripts kun indeholder deres eget indhold.
- **Statistikken regnes efter i koden.** Kvartiler efter dansk skolemetode,
  frekvenser der skal summe til præcis 100 % og grader til 360°, og
  sumkurvens aflæsninger ved lineær interpolation — samme måde som ungen går
  på papiret. Alle atten facitlister har samme sidetal som før, og indholdet
  er sammenlignet token for token med de gamle PDF'er.
- **Kun quizzernes facit mangler nu en kilde:** `facit-statistik-online.pdf`,
  `facitark-manipulation.pdf` og `facitark-funktioner-og-ligninger.html`.
  Dertil ser `facit-statistik-hjemmeopgaver.pdf` og
  `facit-lektier-manipulation.pdf` forældede ud — begge hører til materiale,
  der er erstattet. De er ikke slettet.
- **Resten af sitets grafer er gennemgået.** De øvrige figurer på siden kommer
  fra `figurer.py` og er korrekte; aflæsningsfiguren (`y = x`) er håndtegnet,
  men efterregnet rigtig og har tal på akserne.

---

## Rettet 28. september 2026

- **Det endelige spørgeskema ligger i `spoergeskema/byg_skema_endeligt.gs`.**
  Arket havde 41 linjer fra 19 unger med dubletter, blandet du/Sie og
  Auswahl uden muligheder. Listen er gennemgået og står nu i scriptet selv:
  31 spørgsmål (9 ja/nej, 9 valg med muligheder, 13 fritekst, ikke påkrævet)
  plus alder og køn. "Magst du Bier?" er med efter brugerens valg.
  Brugeren kører `bygEndeligtSkema` fra arkets Apps Script; Code-feltet
  beholdes, så det forudfyldte link og QR-kortene holder. Det gamle
  `byg_formular.gs` (bygger af arket) ligger stadig.

## Rettet 2. oktober 2026

- **Turen er taget ned.** Dagen efter studieturen er `sturmflut.html`, de fem
  gruppesider, de fem gruppe-PDF'er, delebilledet og skærmbilledet af
  Teams-mapperne slettet fra sitet, og adresserne `/sturmflut`,
  `/sturmflut/1–5` og `/hafencity` er fjernet fra `vercel.json`. Kortet på
  tysksiden er væk. Opgaverne er altså ikke længere offentligt tilgængelige.
- **Beholdt:** `claude/byg_sturmflut.py` med en note om nedtagningen, og
  `vejledning/sturmflut-dansk.pdf` med alle opgaver på begge sprog. Begge
  mapper er udelukket fra deploy, så turen kan bygges igen næste år uden at
  ligge offentligt i mellemtiden.

## Rettet 30. september 2026 · Hamborg

- **Turen hedder nu `/sturmflut`** og har fem gruppesider: `/sturmflut/1` til
  `/sturmflut/5`. Ingen printer på turen, så arkene er blevet til mobilsider
  med store afkrydsningsfelter, der huskes i telefonen (localStorage pr.
  gruppe). Læreren deler ét link i Teams; hver gruppe trykker på sit nummer.
- **Opgaverne står på tysk**, så ungerne skal oversætte dem for at kunne løse
  dem. En ordliste på 18 ord giver dem det, man ikke kan gætte — Dammbalken,
  Fluttor, Warft. Den danske udgave med begge sprog side om side ligger i
  `vejledning/sturmflut-dansk.pdf` og udgives ikke.
- **Alle stop er gratis.** Ruten er tjekket igennem for entré; sidste stop,
  Hafen.City.Horizonte, har gratis adgang (bekræftet hos hafencity.com).
- **Hotellet er slået op og lagt ind i modellen** (a&o Hauptbahnhof,
  Amsinckstraße). Det ligger i den østlige ende, tæt på Lohsepark — mit flade
  overslag på 30 minutters gang til Speicherstadt var både forkert og
  misvisende: der er 11 minutter til Lohsepark og 25 til Dalmannkai. Gangen
  fra hotellet regnes nu pr. gruppe.
- **Ruterne er optimeret, ikke valgt.** For hvert startsted regnes alle 120
  rækkefølger igennem; den korteste vælges, og ved lige lange foretrækkes den,
  der slutter tættest på mødestedet. Fire af de fem ruter slutter præcis ved
  Magellan-Terrassen, den femte 200 m derfra — der er en assert på det, for en
  gruppe, der slutter to kilometer væk klokken 14.30, er en dårlig idé,
  uanset hvad regnestykket siger.
- **Gruppesiderne kan printes.** Print-CSS folder alle emner og opgaver ud,
  skalerer de to figurer ned og skjuler knapper og links. Folderne åbnes af
  `beforeprint` og sættes tilbage af `afterprint`, for browseren skjuler ellers
  indholdet i en lukket `<details>`, uanset hvad CSS siger. Siderne er også
  gengivet som PDF i `materiale/sturmflut-gruppe1–5.pdf`, fire sider hver.
- **Siderne har fået et delebillede.** Uden `og:image` vælger Teams selv det
  første billede på siden — og det blev skærmbilledet af mapperne. Nu gengives
  tværsnittet som PNG i 1200×630 (`materiale/sturmflut-delebillede.png`), og
  både forsiden og de fem gruppesider har og:title, og:description, og:url og
  og:image. Bemærk at Teams cacher link-visninger: et link, der allerede er
  slået op, beholder det gamle billede.
- **Skærmbilledet af Teams-mapperne** ligger ved fotoreglerne på alle fem
  gruppesider og på forsiden, så der ikke er tvivl om, hvor billederne skal
  hen. Hver gruppeside nævner gruppens egen mappe ved navn.
- **Kort til hver gruppe.** `figurer.py` har fået `rutekort()`: et skematisk
  kort tegnet af rigtige koordinater, med gruppens egen rute, pile, grøn ring
  ved start, rød ved slut, målestok og nordpil. Vandet er ikke tegnet — kortet
  viser afstande og retninger, ikke gader, og det står på kortet.
- **Koordinaterne er slået op i OpenStreetMap** (Nominatim) og har afløst mit
  eget overslag over afstandene. Gangafstand = fugleflugt × 1,3, rundet til
  nærmeste 50 m. Det flyttede ruterne fra 4,4–4,8 km til 4,5–5,0 km, og
  luften fra 30–40 til 32–38 minutter — hele tidsplanen hvilede på tal, jeg
  havde gættet.
- **Grupperne sendes på tværs.** Hver gruppe har sit eget startsted og sin
  egen rækkefølge af de fem steder — fem forskellige ruter, så to grupper med
  samme emne kommer hjem med forskellige billeder.
- **Alt går til fods — også ud til startstedet.** Vejen fra hotellet ud til
  gruppens eget startsted er nu med i regnskabet; den var overset, og
  grupperne starter op til 2 km fra hinanden. Resultatet: fire grupper går
  5,2 km og gruppe 1 går 4,4 km. At de er lige lange er geometri, ikke held —
  alle går reelt fra Speicherstadt, rundt om det hele og tilbage til
  mødestedet. Luften er 30–40 minutter. Det eneste tal, der er gættet, er de
  30 minutters gang fra hotellet; det står som én konstant i scriptet.
- **Ingen ubahn.** Det kræver, at hver rute *slutter* ved
  mødestedet i stedet for at skulle nå tilbage. Afstandene regnes af en simpel
  model: HafenCity som én akse fra Speicherstadt (0 m) til Baakenhafen
  (2050 m), med Dalmannkai som en stikvej 350 m ude fra Sandtorhafen. Ruterne
  er 3,1–4,8 km.
- **Regnskabet føres pr. gruppe**, ikke for turen under ét — ruterne er
  forskellige, så luften er det også. Scriptet nægter at skrive filerne, hvis
  den strammeste gruppe har under 25 minutters luft. Det fangede to udgaver i
  træk: først 24 minutter, så 20. Stederne og frokosten er strammet, til alle
  fem ruter kunne nås; nu er luften 35–56 minutter.
- **Dagen er fem selvstændige fotosafarier**, ikke én fælles rute. Fælles
  afgang 10.00, fælles opsamling 14.30 ved Magellan-Terrassen. Grupperne
  bestemmer selv rækkefølgen af de fem steder; gruppe 1–3 starter i vest,
  gruppe 4–5 tager U4 mod øst, så de ikke står i kø ved det samme motiv.
  Frokosten sørger de selv for, men gruppen spiser sammen.
  Scriptet regner dagen igennem og nægter at skrive filerne, hvis der er
  mindre end en halv times luft: 270 minutter til rådighed, 230 brugt.
- **Billederne lægges i Teams løbende**, efter hvert stop — ikke om aftenen. De voksne skal kunne følge med undervejs.
- Kort på tysksiden.
- **`claude/tjek.py` kender nu `vercel.json`.** Links som `/sturmflut/3` er
  gyldige, selv om der ikke findes en fil af det navn — til gengæld tjekkes
  det, at hver omskrivning peger på en fil, der findes. Den fandt en fejl med
  det samme: `/hafencity` pegede stadig på en fil, jeg lige havde slettet.

## Rettet 30. september 2026 · Hamborg (første udgave)

- **Tur i HafenCity: `hafencity.html` på `/hafencity`.** Fire timer med
  frokost, seks stop fra Speicherstadt til Baakenhafen, om at bygge og bo uden
  for diget. Fem grupper med hvert sit fotoemne, så billederne kan lægges
  sammen til én fortælling i stedet for fem ens. Gruppeark til print: ét A4
  pr. gruppe med emne, rute til afkrydsning og fotoregler.
- **Tallene er slået efter, ikke husket.** Warften ligger 7,5–8,5 m over NHN,
  promenaderne på de gamle kajers niveau. Stormfloden 1962 stod 5,70 m ved
  Pegel St. Pauli, 1976 stod 6,45 m — højere, men digerne holdt. Tværsnittet
  tegnes af de samme tal, så de to stormfloder havner præcis dér, hvor de
  hører hjemme: over promenaden, under warften. Det er hele pointen i turen.
- **Fangede en ændring undervejs:** HafenCitys InfoCenter i Kesselhaus lukkede
  19. marts 2026 og er flyttet til Baakenallee 33 under navnet
  Hafen.City.Horizonte — åbent torsdag 10–16, gratis. Det gamle sted stod
  stadig i de fleste søgeresultater. Turen slutter det nye sted, ved modellen
  i 1:500.
- **Nyt i figurbiblioteket:** `vandstandssnit()` — tværsnit med promenade,
  warft og historiske vandstande, hvor alt skaleres af de samme meter.

## Rettet 30. september 2026

- **ART-forløb om vredeshåndtering: `socialisering.html` på `/socialisering`.**
  Kropslige tegn og dæmpere, 45 minutter, til grupper på 4–8 deltagere.
  Brugerens eget materiale er kernen — lektionsplan, fire rollespilskort,
  vredeslog og observatørskema — sat op som side og som rigtige filer.
- **`claude/byg_socialisering.py`** bygger siden, materialesættet (PDF og
  Word), udklipsarket med kortene og arbejdsarket. Materialet står ét sted i
  scriptet, så et rollespilskort ikke kan stå på siden og mangle i udklipsarket.
- **Kortene kræver ikke dobbeltsidet print.** Bagsiden trykkes vendt 180
  grader under forsiden; kortet klippes ud i ét stykke og foldes på midten.
  Så kan for- og bagside ikke komme til at sidde skævt i forhold til hinanden.
- **Nyt i figurbiblioteket:** `vredeskurve()` (logistisk kurve med det vindue,
  hvor dæmperne virker), `kropstegn()` (advarselstegn placeret på en figur) og
  `aandedraet()` (faser tegnet med bredde efter varighed).
- `vercel.json` har fået en rewrite mere, så `/socialisering` virker uden
  `.html`. Siden har ikke noget kort på forsiden — den står for sig selv.

## Rettet 24. september 2026

- **Video på tysk-siden:** Peter Hoffmann (klassens tysklærer) viser, hvordan
  man spørger på tysk, om en person vil udfylde skemaet. Hentet fra brugerens
  Drev (19 sekunder, 1080×1440, 75 MB), skrumpet til 720×960, 3,3 MB:
  `materiale/peter-hoffmann-spoerg-paa-tysk.mp4` + plakatbillede. Ligger på
  `tysk.html` og under "Din QR-kode" på projektsiden (`.video`-blok i
  `byg_spoergeskema.py`). Skrumpes med ffmpeg fra `pip install imageio-ffmpeg`.
  Peter Hoffmann er indforstået med, at videoen ligger offentligt (24.9.).
- **Vurderingsskema til projektopgaven** i `vejledning/`, som PDF og Word.
  Bygget af `claude/byg_vurderingsskema.py`, hvor kriterierne står ét sted:
  afkrydsningsskemaet, profilen og niveaubeskrivelserne bygges alle af den
  samme liste, så et kriterium ikke kan stå ét sted og mangle et andet. Tre
  områder — arbejdsprocessen, produktet og fremlæggelsen — 16 kriterier, fire
  niveauer, og de syv karaktertrin.
- **`claude/byg_vejledning_docx.py` forstår nu spaltebredder.** Den læser
  `<col style="width:…%">` og giver Word de samme proportioner som
  HTML-udgaven. Uden det blev et skema med smalle afkrydsningsfelter til
  seks lige brede spalter i Word.

## Rettet 23. september 2026

- **Plastik-forløbet:** bioplast er nu forsøg 2 (0:45–1:45) og
  plastsorteringen forsøg 3 (2:00–2:45), så filmen tørrer resten af dagen.
  Bioplasten varmes i mikroovn: 2 minutter i alt, 4 × 30 sekunder med omrøring
  tre gange undervejs. Kogepladen er ude af udstyrslisten. Side, ungeark-PDF,
  vejledning-PDF og Word er bygget om.

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
6. **En absolut adresse til sitets eget domæne er altid en fejl.** Den virker,
   lige indtil domænet skifter, og så virker den i stilhed forkert. Skriv
   relativt, eller læg adressen ét sted, alt andet læser fra. Lært ved
   domæneskiftet 3.11.
7. **Mål i den rigtige grænseflade, ikke i hukommelsen.** Trin 1 i
   GeoGebra-vejledningen blev forkert to gange: først skrevet af hukommelsen,
   så målt på et besøg, hvor der allerede var klikket. Afhænger noget af, om
   det er første besøg, skal der måles i en frisk browserkontekst.
8. **Slå op i dokumentet, før det får et kort.** Den første formelsamling, der
   blev lagt op, var til gymnasiet. Filnavnet sagde «formelsamling»; niveauet
   stod kun på side 1.
