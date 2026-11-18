# -*- coding: utf-8 -*-
"""Bygger samfundsfagstest.html - 60 multiple choice-spørgsmål.

Siden kører på husets quizmotor, løftet ud af statistik.html ligesom
boksplot.html gør det. Kun STORAGE_KEY og modulnavnene byttes ud.

**Alle tal er slået op 17.11.2026, ikke husket.** De står som konstanter
nedenfor med kilde og dato. Mandatfordelingen kontrolleres af asserts:
summen skal give 179, regeringens fire partier skal give 82, og flertal
skal være 90. Et tal, der ikke passer, stopper bygningen.

    python3 claude/byg_samfundsfagstest.py
"""
import html
import os
import random
import re
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)
import figurer as FG

# Siden er ikke udgivet endnu. kommende/ er udelukket i .vercelignore,
# saa testen kan bygges og ses lokalt uden at ligge paa 321flyv.com.
UD = os.path.join(ROD, 'kommende', 'samfundsfagstest.html')
SKABELON = os.path.join(ROD, 'statistik.html')
OPDATERET = '17. november 2026'

# ====================================================================== tal
# Folketingsvalget 24.3.2026. Kilde: Folketinget og Danmarks Statistik.
MANDATER = [
    ('Ø', 11, '#8b1a2b'), ('ALT', 5, '#1a8f5e'), ('SF', 20, '#b5003c'),
    ('S', 38, '#c8103c'), ('RV', 10, '#7a4fbf'), ('M', 14, '#9b6ce0'),
    ('BP', 4, '#8a8f9c'), ('K', 13, '#0a5a3c'), ('V', 18, '#1f6fd6'),
    ('LA', 16, '#0b7fb5'), ('DD', 10, '#0b4f8a'), ('DF', 16, '#b5710a'),
    ('Nordatlanten', 4, '#586074'),
]
I_ALT = sum(m for _, m, _ in MANDATER)
FLERTAL = 90
REGERING = ('S', 'SF', 'M', 'RV')
REG_MANDATER = sum(m for n, m, _ in MANDATER if n in REGERING)
assert I_ALT == 179, f'der skal være 179 mandater, der er {I_ALT}'
assert REG_MANDATER == 82, f'regeringen har {REG_MANDATER}, ikke 82'
assert FLERTAL == I_ALT // 2 + 1
assert REG_MANDATER < FLERTAL, 'regeringen er et mindretal — det er pointen'

INFLATION = 2.2          # okt. 2026, Danmarks Statistik 10.11.2026
KERNEINFLATION = 1.7     # samme kilde
BETALINGSBALANCE = 441   # mia. kr., 2025, Danmarks Statistik
BB_PCT = 14              # pct. af BNP, samme kilde
BNP = 3000               # ca. mia. kr. om året (ca. 750 mia. pr. kvartal)
FINANSLOV = 950          # mia. kr., statens nettoudgifter §1-36
EU_LANDE = 27
OECD_LANDE = 38

# svarenes placering: 20 gange ABC i tilfældig orden, fast frø.
# Det giver præcis 20 af hvert bogstav, uden at mønstret kan gættes.
_r = random.Random(9)
ORDEN = []
for _ in range(20):
    b = [0, 1, 2]
    _r.shuffle(b)
    ORDEN += b
# der laves 60 pladser; de foerste ANTAL bruges, resten ligger ubrugt
assert len(ORDEN) == 60 and all(ORDEN.count(i) == 20 for i in range(3))


# ================================================================= figurer
F_SAL = FG.folketingssal(MANDATER, titel='Folketinget efter valget 24. marts 2026',
                         flertal=FLERTAL)
F_REGERING = FG.soejler(
    [38, 20, 14, 10], ['S', 'SF', 'M', 'RV'],
    titel=f'Regeringens fire partier · {REG_MANDATER} mandater i alt',
    ynavn='mandater', W=460, H=250)
F_AKSE = FG.hoejre_venstre([
    ('Enhedslisten', -0.95, '#8b1a2b'), ('SF', -0.62, '#b5003c'),
    ('Alternativet', -0.80, '#1a8f5e'), ('Socialdemokratiet', -0.38, '#c8103c'),
    ('Radikale', -0.15, '#7a4fbf'), ('Moderaterne', 0.08, '#9b6ce0'),
    ('Konservative', 0.45, '#0a5a3c'), ('Venstre', 0.52, '#1f6fd6'),
    ('Dansk Folkeparti', 0.62, '#b5710a'),
    ('Liberal Alliance', 0.92, '#0b7fb5')],
    titel='Partierne på en højre-venstre-akse')

F_LOV = FG.procesdiagram([
    ('Ministeriet', 'Udkast, høring og høringsnotat', 'a'),
    ('Fremsættelse', 'Forslaget får et L-nummer og bliver offentligt', 'b'),
    ('1. behandling', 'Debat om hovedidéen — derefter i udvalg', 'b'),
    ('Udvalgsbehandling', 'Spørgsmål, ændringsforslag og betænkning', 'b'),
    ('2. behandling', 'Debat om detaljerne og afstemning om ændringer', 'b'),
    ('3. behandling', 'Sidste afstemning om hele forslaget', 'b'),
    ('Stadfæstelse', 'Kundgøres i Lovtidende og træder i kraft', 'c'),
], farver={'a': FG.MUT, 'b': FG.BLA, 'c': FG.GRO},
   legende=[('Ministeriet', 'a'), ('Folketinget', 'b'), ('Efter vedtagelsen', 'c')])

F_LOV_KORT = FG.procesdiagram([
    ('Ministeriet', '', 'a'),
    ('Fremsættelse', '', 'b'),
    ('1. behandling', '', 'b'),
    ('Udvalgsbehandling', '', 'b'),
    ('2. behandling', '', 'b'),
    ('3. behandling', '', 'b'),
    ('Stadfæstelse', '', 'c'),
], W=560, farver={'a': FG.MUT, 'b': FG.BLA, 'c': FG.GRO})

F_RINGE = FG.socialisationsringe([
    ('Primær', '#c23b4b', ''), ('Sekundær', '#1f6fd6', ''),
    ('Tertiær', '#b5710a', '')])
F_KRYDS = FG.krydspres([('Hjemme', ''), ('I klassen', ''),
                        ('I feedet', '')])
F_NORM = FG.procesdiagram([
    ('Normen', 'Det, de fleste gør — og regner med at du også gør', 'n'),
    ('Bruddet', 'Nogen gør noget andet', 'n'),
    ('Sanktionen', 'Et blik, et grin, en kommentar — eller ros', 'r'),
    ('Normen står fast', 'Nu ved alle, hvor grænsen går', 'n'),
], farver={'n': FG.BLA, 'r': FG.ROD})

F_SKAERM = FG.soejler([27, 28, 16], ['15–19 år', '20–29 år', 'Hele befolkningen'],
                      titel='Over 6 timers skærm om dagen · Danmark 2026',
                      ynavn='%', W=480, H=260,
                      farve=[FG.BLA, FG.BLA, FG.MUT])
F_SKOLE = FG.soejler([3.8, 2], ['Danmark', 'OECD-snit'],
                     titel='Digitale redskaber i skoletiden · timer om dagen',
                     ynavn='timer', W=420, H=250)
F_PROBLEM = FG.soejler([7, 11], ['2018', '2022'],
                       titel='Problematisk brug af sociale medier · 44 lande',
                       ynavn='%', W=400, H=240)
F_FORMEGET = FG.soejler([25, 35, 40], ['8–12 år', '13–17 år', '18–25 år'],
                        titel='Synes selv, de bruger for meget tid · 2025',
                        ynavn='%', W=460, H=250)
F_KOEN = FG.soejler([13, 9, 7, 16], ['Piger·SoMe', 'Drenge·SoMe',
                                     'Piger·gaming', 'Drenge·gaming'],
                    titel='Problematisk brug fordelt på køn · 2022',
                    ynavn='%', W=480, H=250,
                    farve=['#c23b4b', FG.BLA, '#c23b4b', FG.BLA])

F_LLM = FG.procesdiagram([
    ('Du skriver', 'Din tekst deles i tokens, dvs. små stykker ord.', 'i'),
    ('Modellen regner', 'Hvilket token er mest sandsynligt som det næste?', 'k'),
    ('Ét token ad gangen', 'Den skriver det og regner forfra.', 'k'),
    ('Du læser et svar', 'Det ser ud, som om nogen har tænkt.', 'u'),
], farver={'i': FG.MUT, 'k': FG.BLA, 'u': FG.GRO})
F_AGENT = FG.procesdiagram([
    ('Mål', 'En opgave, ikke et spørgsmål.', 'i'),
    ('Tænk', 'Modellen vælger selv næste skridt.', 'k'),
    ('Brug et værktøj', 'Søg, skriv en fil, send noget.', 'k'),
    ('Menneske i løkken', 'Nogen godkender det, der ikke kan fortrydes.', 's'),
], farver={'i': FG.MUT, 'k': FG.BLA, 's': FG.ROD})
F_NORM_KORT = FG.procesdiagram([
    ('Normen', '', 'n'), ('Bruddet', '', 'n'),
    ('Sanktionen', '', 'r'), ('Normen står fast', '', 'n'),
], W=540, farver={'n': FG.BLA, 'r': FG.ROD})
F_LLM_KORT = FG.procesdiagram([
    ('Du skriver', '', 'i'), ('Modellen regner', '', 'k'),
    ('Ét token ad gangen', '', 'k'), ('Du læser et svar', '', 'u'),
], W=540, farver={'i': FG.MUT, 'k': FG.BLA, 'u': FG.GRO})
F_AGENT_KORT = FG.procesdiagram([
    ('Mål', '', 'i'), ('Tænk', '', 'k'),
    ('Brug et værktøj', '', 'k'), ('Menneske i løkken', '', 's'),
], W=540, farver={'i': FG.MUT, 'k': FG.BLA, 's': FG.ROD})
F_AIBRUG = FG.soejler([1000, 950, 382, 167, 150, 130, 117],
                      ['Meta AI', 'Gemini', 'Doubao', 'Qwen', 'Copilot',
                       'DeepSeek', 'Grok'],
                      titel='Brugere om måneden · mio.', ynavn='millioner',
                      W=560, H=280)
F_EJERE = FG.cirkeldiagram([('Ansatte og investorer', 47), ('Microsoft', 27),
                            ('OpenAI Foundation', 26)])
F_CHIP = FG.cirkeldiagram([('Nvidia', 81), ('AMD', 10), ('Alle andre', 9)])

F_OEKONOMI = FG.soejler([BNP, FINANSLOV, BETALINGSBALANCE],
                        ['BNP', 'Finansloven', 'Betalingsbalance'],
                        titel='Tre tal om dansk økonomi · mia. kr.',
                        ynavn='mia. kr.', W=480, H=270,
                        farve=[FG.BLA, FG.ORA, FG.GRO])
F_INFLATION = FG.soejler([INFLATION, KERNEINFLATION],
                         ['Inflation', 'Kerneinflation'],
                         titel='Prisstigning på et år · oktober 2026',
                         ynavn='%', W=400, H=240,
                         farve=[FG.BLA, FG.MUT])
F_KLUBBER = FG.soejler([EU_LANDE, OECD_LANDE], ['EU', 'OECD'],
                       titel='Hvor mange lande er med?', ynavn='lande',
                       W=380, H=240, farve=[FG.BLA, FG.GRO])


# =============================================================== spørgsmål
# (figur, spørgsmål, niveau, rigtigt svar, to forkerte, forklaring)
# Hverken spørgsmål eller forklaring må indeholde et citationstegn — de
# ligger i HTML-attributter. byg_spm har en assert på det.

SPM_TEKST = [
 (F_LOV_KORT, 'Hvor mange gange skal et lovforslag behandles i Folketinget, '
  'før det kan vedtages?', 'Lovprocessen', 'Tre gange',
  ('To gange', 'Én gang'),
  'Det står i grundlovens § 41. Mellem behandlingerne skal der gå mindst '
  'to dage — det står i Folketingets forretningsorden.'),
 (F_LOV_KORT, 'Hvad er et høringssvar?', 'Lovprocessen',
  'Det, en organisation eller kommune svarer, når den har læst udkastet',
  ('Ministerens svar på et spørgsmål fra et udvalg',
   'Den endelige afstemning om lovforslaget'),
  'Høringssvarene er offentlige. Det er dér, man kan se, hvem der prøver '
  'at påvirke loven, og hvad de vil have ændret.'),
 (F_LOV_KORT, 'Hvad sker der ved 1. behandling?', 'Lovprocessen',
  'Der debatteres om forslagets hovedidé, og så sendes det i udvalg',
  ('Der stemmes om hver enkelt paragraf',
   'Loven skrives under af monarken'),
  'Ved 1. behandling stemmes der ikke om indholdet. Det er idéen, der '
  'diskuteres — detaljerne kommer ved 2. behandling.'),
 (F_LOV_KORT, 'Hvor i lovprocessen sker det meste af arbejdet?', 'Lovprocessen',
  'I udvalgsbehandlingen mellem 1. og 2. behandling',
  ('I folketingssalen ved 3. behandling', 'Ved den kongelige stadfæstelse'),
  'Udvalget stiller skriftlige spørgsmål til ministeren, kan kalde '
  'eksperter ind, og partierne stiller ændringsforslag. Til sidst skriver '
  'udvalget en betænkning.'),
 (F_LOV_KORT, 'Hvad er et L-nummer?', 'Lovprocessen',
  'Lovforslagets nummer i Folketinget, fx L 42',
  ('Nummeret på den lov, der bliver trykt i Lovtidende',
   'Nummeret på det udvalg, der behandler forslaget'),
  'Nummeret gør det muligt at følge præcis det ene forslag på ft.dk: '
  'teksten, spørgsmålene og senere afstemningen.'),
 (F_LOV_KORT, 'Hvor stor en del af Folketingets medlemmer kan kræve en vedtaget '
  'lov sendt til folkeafstemning?', 'Lovprocessen', 'En tredjedel',
  ('Et flertal', 'To tredjedele'),
  'Det står i grundlovens § 42. Nogle love er undtaget — blandt andet '
  'finanslove og skattelove.'),
 (F_RINGE, 'Hvad betyder navnene primær, sekundær og tertiær socialisering?',
  'Socialisering', 'Rækkefølgen — hvad der kom først i ens liv',
  ('Hvor vigtig arenaen er', 'Hvor mange timer man bruger der'),
  'Den primære arena var der, før du kunne vælge noget som helst. '
  'Navnene siger intet om, hvad der betyder mest i dag.'),
 ('', 'Hvad er en social sanktion?', 'Socialisering',
  'Den reaktion, der kommer, når nogen bryder en norm',
  ('En skreven regel, der hænger på væggen',
   'En straf, der gives af en myndighed'),
  'Sanktioner er sjældent straf. Det er et blik, en pause, et grin — '
  'eller ros og et like, som er en positiv sanktion.'),
]

SPM_DIGITAL = [
 ('', 'Hvor stor en andel af de 15–19-årige har over 6 timers skærm '
  'om dagen?', 'Paratviden', '27 %', ('16 %', '72 %'),
  'Tallet er fra Danmarks Statistik, 31. august 2026. Det dækker al '
  'skærmtid: mobil, computer, tv og spil — ikke kun sociale medier.'),
 (F_SKAERM, 'Hvilken gruppe på figuren har den højeste andel med over '
  '6 timers skærm?', 'Aflæs', 'De 20–29-årige', ('De 15–19-årige',
  'Hele befolkningen'),
  'Det er en fælde. De 20–29-årige ligger på 28 % og altså lidt over de '
  '15–19-åriges 27 %. De unge er ikke dem, der sidder længst.'),
 (F_SKAERM, 'Hvorfor har den grå søjle sin egen farve?', 'Forstå',
  'Fordi den ikke er en aldersgruppe, men alle danskere lagt sammen',
  ('Fordi tallet er fra et andet år', 'Fordi tallet er usikkert'),
  'Hele befolkningen fra 15 til 89 år er ét samlet tal. Sættes den som '
  'en tredje søjle i samme farve, læses den som en tredje aldersgruppe.'),
 ('', 'Hvor mange timer om dagen bruger danske 15-årige digitale '
  'redskaber i skoletiden?', 'Paratviden', '3,8 timer', ('2 timer', '6 timer'),
  'Det er det højeste af alle 81 lande i PISA 2022 — næsten det dobbelte '
  'af OECD-gennemsnittet på 2 timer.'),
 ('', 'Hvor stor en del af de danske elever bruger digitale redskaber '
  'i hver time eller næsten hver time?', 'Paratviden', '72 %',
  ('16 %', '38 %'), 'I OECD som helhed er tallet 16 %. Det er dér, '
  'Danmark for alvor skiller sig ud — ikke på fritidsforbruget.'),
 ('', 'Hvordan udviklede problematisk brug af sociale medier sig '
  'fra 2018 til 2022 i de 44 lande?', 'Aflæs',
  'Fra 7 % til 11 %', ('Fra 11 % til 7 %', 'Den var uændret'),
  'Kilden er WHO Europa, 25. september 2024. Problematisk brug betyder, '
  'at den unge har mistet kontrollen — ikke bare at der bruges lang tid.'),
 ('', 'Hvad betyder det i undersøgelsen, at brugen er problematisk?',
  'Forstå', 'At den unge har mistet kontrollen over den',
  ('At den unge bruger mere end 6 timer om dagen',
   'At forældrene synes, det er for meget'),
  'Kan ikke lade være, forsømmer andet, får det dårligt uden. Lang tid '
  'er ikke i sig selv problematisk brug.'),
 ('', 'Hvad viser tallene for piger og drenge?', 'Forstå',
  'Piger ligger højest på sociale medier, drenge højest på gaming',
  ('Piger ligger højest på begge dele', 'Drenge ligger højest på begge dele'),
  'Sociale medier: 13 % mod 9 %. Gaming: 16 % mod 7 %. Et samlet tal for '
  'unge skjuler to forskellige mønstre.'),
 ('', 'Hvilken aldersgruppe synes selv, at flest af dem bruger for '
  'meget tid på sociale medier?', 'Aflæs', 'De 18–25-årige',
  ('De 8–12-årige', 'De 13–17-årige'),
  '40 % mod 35 % og 25 %. Jo ældre, jo mere kritiske er de unge selv — '
  'det er ikke kun voksne, der synes, der er et problem.'),
 ('', 'Australien forbød sociale medier for børn under 16 i '
  'december 2025. Hvad viste målingen tre måneder efter?', 'Forstå',
  'At 8 ud af 10 australske teenagere under 16 stadig brugte dem',
  ('At næsten ingen brugte dem længere',
   'At brugen var steget efter forbuddet'),
  'Andelen med egen konto faldt fra 52 % til 42 %. Et fald, men ikke et '
  'stop. En lov er ikke det samme som en virkning.'),
]

SPM_AI = [
 (F_LLM_KORT, 'Hvad er en stor sprogmodel (LLM) trænet til at gøre?', 'AI-ordbog',
  'At gætte det næste stykke tekst',
  ('At slå svar op i en database', 'At oversætte mellem to sprog'),
  'Den slår ikke op og tænker ikke efter. Den regner ud, hvad der er '
  'mest sandsynligt som det næste — og skriver det, ét token ad gangen.'),
 (F_LLM_KORT, 'Hvad er et token?', 'AI-ordbog',
  'Et kort ord eller en orddel — det stykke tekst, modellen regner i',
  ('En adgangskode til en AI-tjeneste', 'Et helt afsnit tekst'),
  'Priser på AI opgøres i tokens, ikke i ord. Ordet Fyrtøjet kan blive '
  'til to-tre tokens.'),
 (F_LLM_KORT, 'Hvad er en hallucination?', 'AI-ordbog',
  'Når modellen finder på noget, der lyder rigtigt, men ikke er det',
  ('Når modellen nægter at svare', 'Når modellen laver et billede'),
  'Det vigtigste ord på listen. Modellen gætter det næste ord; den slår '
  'ikke op. Tjek altid et tal, et navn og en kilde.'),
 (F_LLM_KORT, 'Hvad er et kontekstvindue?', 'AI-ordbog',
  'Hvor meget modellen kan have for øje på én gang',
  ('Det vindue, chatten vises i', 'Hvor mange brugere der kan være på'),
  'Er vinduet fyldt, falder det ældste ud. Det er derfor en lang samtale '
  'kan glemme noget, du skrev i starten.'),
 (F_AGENT_KORT, 'Hvad er forskellen på en chatbot og en agent?', 'AI-ordbog',
  'Agenten får lov at handle — søge, skrive filer, sende noget',
  ('Agenten er hurtigere end en chatbot',
   'Agenten bruger ikke en sprogmodel'),
  'Det er modellen plus nogle værktøjer plus lov til at bruge dem. '
  'Den bliver ved i en løkke, til opgaven er løst.'),
 (F_AGENT_KORT, 'Hvad betyder menneske i løkken?', 'AI-ordbog',
  'At et menneske skal godkende, før agenten gør noget, der ikke kan fortrydes',
  ('At en person skriver svarene i stedet for modellen',
   'At modellen er trænet af mennesker'),
  'Sende, slette, betale. Den vigtigste sikring der findes — spørg altid, '
  'hvem der godkender.'),
 ('', 'Hvad er edge AI?', 'AI-ordbog',
  'AI, der kører på selve enheden i stedet for i et datacenter',
  ('AI, der kun bruges af virksomheder', 'Den nyeste version af en model'),
  'Edge betyder kanten af nettet — altså ude hos dig. Det er hurtigere, '
  'virker uden net, og dine data forlader ikke dimsen.'),
 ('', 'ChatGPTs og Geminis brugertal kan ikke sammenlignes direkte. '
  'Hvorfor ikke?', 'Kildekritik',
  'Fordi OpenAI opgør sine brugere pr. uge og Google pr. måned',
  ('Fordi ChatGPT har for få brugere',
   'Fordi OpenAI ikke oplyser nogen tal'),
  'En uge og en måned er ikke samme vindue. To tal med forskellig enhed '
  'kan ikke sammenlignes, selv om begge hedder brugere.'),
 (F_EJERE, 'Hvem har kontrollen over OpenAI?', 'AI-ordbog',
  'OpenAI Foundation, fordi fonden udpeger bestyrelsen',
  ('Microsoft, fordi de ejer den største andel',
   'De ansatte, fordi de tilsammen ejer mest'),
  'Fonden ejer kun ca. 26 % og Microsoft ca. 27 %. Den, der ejer mest, '
  'er altså ikke den, der bestemmer.'),
 (F_CHIP, 'Hvorfor regnes Nvidia med blandt de største aktører inden for AI?',
  'AI-ordbog', 'Fordi alle de andre køber de chips, deres AI kører på',
  ('Fordi Nvidia har den mest brugte chatbot',
   'Fordi Nvidia ejer en del af OpenAI'),
  'Nvidia sælger ikke AI; de sælger det, AI kører på. Derfor tjener de '
  'penge, uanset hvem der vinder kampen om brugerne.'),
]

SPM_IDEOLOGI = [
 (F_AKSE, 'Hvad er en ideologi?', 'Ideologi',
  'Et sammenhængende sæt idéer om, hvordan samfundet bør indrettes',
  ('En plan for næste års statsbudget',
   'En aftale mellem to partier om en enkelt lov'),
  'En ideologi indeholder et menneskesyn, et samfundssyn og et mål. '
  'Den rækker længere end det enkelte forslag.'),
 (F_AKSE, 'Hvad er kernen i liberalismen?', 'Ideologi',
  'Den enkeltes frihed og ansvar, og en stat der blander sig mindst muligt',
  ('At staten ejer de vigtigste virksomheder',
   'At traditioner skal bevares uændret'),
  'Deraf ønsket om lavere skat, mindre offentlig sektor og mere frit '
  'valg. Liberale partier i Danmark er bl.a. Venstre og Liberal Alliance.'),
 (F_AKSE, 'Hvad er kernen i socialismen?', 'Ideologi',
  'Større økonomisk lighed, blandt andet gennem omfordeling',
  ('At markedet skal bestemme så meget som muligt',
   'At nationens historie er vigtigere end den enkelte'),
  'Midlerne er skat efter evne og velfærd efter behov. Socialdemokratiet, '
  'SF og Enhedslisten hører til denne tradition, men vil forskelligt langt.'),
 (F_AKSE, 'Hvad er kernen i konservatismen?', 'Ideologi',
  'At forandring skal ske langsomt, og at det, der virker, skal bevares',
  ('At alle afgørelser skal træffes ved folkeafstemning',
   'At staten skal eje jorden'),
  'Konservatismen lægger vægt på traditioner, familien, ejendomsretten og '
  'orden — og er skeptisk over for store, hurtige reformer.'),
 ('', 'Hvilket parti ligger længst til venstre i Folketinget?',
  'Paratviden', 'Enhedslisten', ('Socialdemokratiet', 'Radikale Venstre'),
  'Enhedslisten fik 11 mandater ved valget i 2026. Socialdemokratiet er '
  'det største parti på venstrefløjen, men ligger tættere på midten.'),
 (F_AKSE, 'Partiet Venstre ligger på højrefløjen. Hvorfor hedder det så '
  'Venstre?', 'Forstå',
  'Fordi navnet er historisk: partiet sad til venstre i salen i 1870erne',
  ('Fordi partiet stemmer med venstrefløjen i økonomiske spørgsmål',
   'Fordi partiet blev stiftet af en mand ved navn Venstre'),
  'Dengang stod Venstre over for Højre, som var godsejernes parti. '
  'Et partinavn fortæller ikke altid, hvor partiet står i dag.'),
 (F_AKSE, 'Hvad menes der med rød og blå blok?', 'Ideologi',
  'De partier, der normalt peger på hver sin kandidat som statsminister',
  ('De partier, der sidder henholdsvis til venstre og højre i salen',
   'Regeringen over for alle de øvrige partier'),
  'Blokkene er ikke formelle. Efter valget i 2026 kunne ingen af dem '
  'danne regering alene — og regeringen kom til at gå på tværs.'),
 (F_SAL, 'Et parti vil sænke skatten og samtidig skære i den offentlige '
  'sektor. Hvilken ideologi trækker det på?', 'Forstå', 'Liberalisme',
  ('Socialisme', 'Konservatisme'),
  'Lavere skat og mindre stat er det liberale svar. Pas på: et konkret '
  'parti kan godt låne idéer fra flere ideologier på én gang.'),
 (F_SAL, 'Hvad kendetegner den universelle velfærdsmodel, som Danmark '
  'bruger?', 'Ideologi',
  'Ydelser betales af skatten og gælder alle, uanset indkomst',
  ('Man får kun hjælp, hvis man har en forsikring',
   'Kun de fattigste får hjælp fra det offentlige'),
  'Den kaldes også den skandinaviske model. Den bygger på høj skat og '
  'høj beskæftigelse — begge dele skal holde for at den hænger sammen.'),
 (F_SAL, 'Hvad er forskellen på en ideologi og et partiprogram?', 'Forstå',
  'Ideologien er de grundlæggende idéer, programmet er de konkrete forslag',
  ('Der er ingen forskel — det er to ord for det samme',
   'Et partiprogram gælder i flere år, en ideologi kun i én valgperiode'),
  'Derfor kan to partier dele ideologi og alligevel være uenige om en '
  'konkret lov — og omvendt stemme ens ud fra hver sin ideologi.'),
]

SPM_REGERING = [
 (F_SAL, 'Hvor mange mandater er der i Folketinget?', 'Paratviden',
  '179', ('175', '180'),
  'De 175 vælges i Danmark. Færøerne og Grønland vælger to hver — '
  'det er derfor, tallet er 179 og ikke 175.'),
 ('', 'Hvor mange mandater skal der til for at have flertal?',
  'Paratviden', '90', ('89', '91'),
  'Halvdelen af 179 er 89,5 — så flertallet begynder ved 90. Det er '
  'derfor stregen i figuren ligger, hvor den gør.'),
 ('', 'Hvor mange mandater vælges der på Færøerne og i Grønland '
  'tilsammen?', 'Paratviden', '4', ('2', '6'),
  'To fra hvert sted. De nordatlantiske mandater har flere gange været '
  'afgørende for, om en regering havde flertal.'),
 ('', 'Hvornår var der folketingsvalg sidst?', 'Paratviden',
  '24. marts 2026', ('1. november 2022', '5. juni 2025'),
  'Valget i 2022 var det forrige. Der skal være valg mindst hvert '
  'fjerde år, men statsministeren kan udskrive det før tid.'),
 (F_REGERING, 'Hvilke partier sidder i regeringen?', 'Paratviden',
  'Socialdemokratiet, SF, Moderaterne og Radikale Venstre',
  ('Socialdemokratiet, Venstre og Moderaterne',
   'Venstre, Konservative og Liberal Alliance'),
  'Regeringen Mette Frederiksen III tiltrådte 3. juni 2026 — altså '
  'mere end to måneder efter valget. Regeringsdannelse tager tid.'),
 (F_REGERING, 'Hvem er statsminister?', 'Paratviden', 'Mette Frederiksen',
  ('Lars Løkke Rasmussen', 'Peter Hummelgaard'),
  'Mette Frederiksen (S) har været statsminister siden 2019 og fortsatte '
  'efter valget i 2026.'),
 ('', 'Hvor mange mandater har regeringspartierne tilsammen?',
  'Paratviden', '82', ('90', '101'),
  'Det er færre end de 90, der skal til for et flertal. Regeringen er '
  'altså en mindretalsregering og skal finde flertal fra sag til sag.'),
 ('', 'Hvad vil det sige, at Danmark har negativ parlamentarisme?',
  'Forstå', 'En regering kan sidde, så længe der ikke er et flertal imod den',
  ('En regering skal have et flertal bag sig for at kunne sidde',
   'Folketinget kan ikke vælte en regering'),
  'Derfor kan en regering med 82 mandater godt regere. Den skal bare '
  'undgå, at 90 andre stemmer den ned.'),
 ('', 'Hvem er finansminister?', 'Paratviden', 'Peter Hummelgaard',
  ('Nicolai Wammen', 'Pia Olsen Dyhr'),
  'Nicolai Wammen er justitsminister i den nuværende regering, og '
  'Pia Olsen Dyhr er økonomi- og indenrigsminister.'),
 ('', 'Hvem er udenrigsminister?', 'Paratviden',
  'Lars Løkke Rasmussen', ('Mette Frederiksen', 'Troels Lund Poulsen'),
  'Lars Løkke Rasmussen er formand for Moderaterne, som er et af de fire '
  'regeringspartier.'),
]

SPM_OEKONOMI = [
 ('', 'Hvad er BNP?', 'Økonomi',
  'Værdien af alt det, der produceres i et land på et år',
  ('Summen af alle danskeres løn efter skat',
   'Statens samlede udgifter på finansloven'),
  'BNP står for bruttonationalprodukt. Det måler produktionen — ikke '
  'hvor pengene ender, og ikke hvordan de er fordelt.'),
 ('', 'Hvor stort er Danmarks BNP cirka?', 'Økonomi',
  'Omkring 3.000 milliarder kroner om året',
  ('Omkring 300 milliarder kroner om året',
   'Omkring 30.000 milliarder kroner om året'),
  'Cirka 750 milliarder i kvartalet. Det er størrelsesordenen, der '
  'tæller her — ikke decimalerne.'),
 ('', 'Hvorfor er BNP ikke et mål for, hvor godt folk har det?',
  'Forstå', 'Fordi det kun måler produktionen og intet siger om fordelingen',
  ('Fordi det kun opgøres hvert tiende år',
   'Fordi det ikke medregner virksomheder'),
  'To lande kan have samme BNP og helt forskellig ulighed. Derfor '
  'bruges BNP sammen med andre tal, ikke alene.'),
 ('', 'Hvad er inflation?', 'Økonomi',
  'At priserne generelt stiger, så pengene kan købe mindre',
  ('At lønningerne stiger', 'At der bliver trykt flere pengesedler'),
  'Inflationen måles med forbrugerprisindekset, som følger prisen på '
  'en fast kurv af varer og tjenester.'),
 ('', 'Hvor meget steg priserne i Danmark fra oktober 2025 til '
  'oktober 2026?', 'Paratviden', '2,2 %', ('0,5 %', '7,4 %'),
  'Tallet er fra Danmarks Statistik, offentliggjort 10. november 2026. '
  'Fra september til oktober alene steg indekset 0,5 %.'),
 ('', 'Hvad er kerneinflation?', 'Økonomi',
  'Inflationen uden energi og uforarbejdede fødevarer',
  ('Inflationen kun på fødevarer', 'Inflationen målt over ti år'),
  'Energi- og fødevarepriser svinger meget fra måned til måned. '
  'Kerneinflationen viser den mere stabile udvikling — 1,7 % i oktober.'),
 ('', 'Hvad måler betalingsbalancen?', 'Økonomi',
  'Forskellen mellem det, Danmark tjener i udlandet, og det vi betaler dertil',
  ('Forskellen mellem statens indtægter og udgifter',
   'Hvor mange penge danskerne har i banken'),
  'Det er landet over for udlandet. Statens indtægter og udgifter er '
  'noget andet — det er finansloven og det offentlige budget.'),
 ('', 'Danmark havde i 2025 et overskud på betalingsbalancen på '
  'cirka 441 milliarder kroner. Hvad svarer det til?', 'Økonomi',
  'Omkring 14 % af BNP', ('Omkring 2 % af BNP', 'Omkring 45 % af BNP'),
  'Overskuddet er vokset fra 190 mia. kr. i 2018. Et stort og vedvarende '
  'overskud betyder, at Danmark samlet set låner ud til udlandet.'),
 ('', 'Hvor mange lande er med i EU?', 'Paratviden', '27 lande',
  ('25 lande', '31 lande'),
  'Tallet har været 27, siden Storbritannien forlod EU i 2020. '
  'Montenegro er det kandidatland, der er nået længst.'),
 ('', 'Hvor mange lande er med i OECD?', 'Paratviden', '38 lande',
  ('27 lande', '51 lande'),
  'OECD er de rige landes samarbejdsorganisation. Costa Rica kom med '
  'som nr. 38 i 2021. Danmark har været med siden starten i 1961.'),
]

ALLE = [SPM_TEKST, SPM_DIGITAL, SPM_AI, SPM_IDEOLOGI, SPM_REGERING,
        SPM_OEKONOMI]
ANTAL = sum(len(x) for x in ALLE)
assert ANTAL == 58, f'der skal være 58 spørgsmål, der er {ANTAL}'
assert all(6 <= len(x) <= 10 for x in ALLE)
# svarene skal stadig fordele sig nogenlunde jaevnt over A, B og C, ogsaa
# naar antallet ikke gaar op i tre
for _b in range(3):
    assert ORDEN[:ANTAL].count(_b) >= ANTAL // 3 - 1, 'svarene er skæve'


# ------------------------------------------------- figurer til rettearket
# I testen er de fleste figurer taget ud, fordi de roebede svaret. I
# rettearket er svaret allerede givet, og dér er tegningen netop det, der
# goer forklaringen konkret. Her staar, hvilken figur hvert af de
# figurloese spoergsmaal hoerer sammen med.
RETTEARK_FIGUR = {
    8: F_NORM_KORT, 9: F_SKAERM, 12: F_SKOLE, 13: F_SKOLE,
    14: F_PROBLEM, 15: F_PROBLEM, 16: F_KOEN, 17: F_FORMEGET,
    18: F_FORMEGET, 25: F_AGENT_KORT, 26: F_AIBRUG, 33: F_AKSE,
    40: F_SAL, 41: F_SAL, 42: F_SAL, 45: F_REGERING,
    46: F_REGERING, 47: F_REGERING, 48: F_REGERING, 49: F_OEKONOMI,
    50: F_OEKONOMI, 51: F_OEKONOMI, 52: F_INFLATION, 53: F_INFLATION,
    54: F_INFLATION, 55: F_OEKONOMI, 56: F_OEKONOMI, 57: F_KLUBBER,
    58: F_KLUBBER,
}
# De korte procesdiagrammer mistede forklaringen i kasserne, da de skulle
# bruges i en test. I rettearket vises den fulde udgave igen.
FULD_UDGAVE = {F_LOV_KORT: F_LOV, F_NORM_KORT: F_NORM,
               F_LLM_KORT: F_LLM, F_AGENT_KORT: F_AGENT}
assert set(RETTEARK_FIGUR) <= set(range(1, ANTAL + 1))


# =================================================================== siden
def byg_spm(liste, start, orden):
    ud = []
    for k, (fig, tekst, niveau, rigtig, forkerte, forklaring) in enumerate(liste):
        plads = orden[start + k - 1]
        valg = list(forkerte)
        valg.insert(plads, rigtig)
        assert len(set(valg)) == 3, f'spørgsmål {start+k} har ens svarmuligheder'
        assert valg[plads] == rigtig
        assert '"' not in forklaring and '"' not in tekst
        knapper = ' '.join(
            f'<button class="opt"><span class="mk">{"ABC"[j]}</span> '
            f'{html.escape(v, quote=False)}</button>' for j, v in enumerate(valg))
        figur = f'<div class="qfig">{fig}</div>' if fig else ''
        ud.append(
            f'<div class="q" data-answer="{plads}" data-exp="{forklaring}">'
            f'<div class="qtext"><span class="qn">{start+k}.</span> {tekst} '
            f'<span class="lvl">{niveau}</span></div>{figur}'
            f'<div class="opts">{knapper}</div><div class="fb"></div></div>')
    return ''.join(ud)


def quiz(nr, tag, titel, undertitel, krop, antal, slut=None):
    besked = ('<span id="finalMsg"></span>' if slut is None
              else f'<span>{slut}</span>')
    return (f'<section class="quiz" data-quiz id="quiz{nr}">'
            f'<div class="qhead"><span class="qtag">{tag}</span>'
            f'<h3>{titel}</h3></div><p class="qsub">{undertitel}</p>{krop}'
            f'<div class="scorebar"><span class="badge" data-score>'
            f'0 / {antal} rigtige</span> {besked}</div>'
            f'</section>')


MODULER = [
    (1, 'Quiz 1 · teksterne', 'Teksterne', SPM_TEKST,
     'Lovprocessen og socialisering — fra de to tekster, I har læst.',
     'Videre til dataarket om digital socialisering.'),
    (2, 'Quiz 2 · dataarket', 'Digital socialisering', SPM_DIGITAL,
     'Tallene fra dataarket. Flere af spørgsmålene kan kun besvares ved at '
     'læse figuren — ikke ved at huske en overskrift.',
     'Videre til AI-ordbogen.'),
    (3, 'Quiz 3 · AI-ordbogen', 'AI-ordbogen', SPM_AI,
     'Begreberne fra ordbogen: sprogmodeller, agenter og de største aktører.',
     'Videre til partier og ideologi.'),
    (4, 'Quiz 4 · ideologi', 'Partier og ideologi', SPM_IDEOLOGI,
     'De tre klassiske ideologier, højre-venstre-aksen og hvad et partinavn '
     'ikke fortæller. <b>Bemærk:</b> partiernes placering på aksen er et '
     'skøn, ikke en måling — partierne er ikke selv enige om den. Det er '
     'rækkefølgen i grove træk, I skal kunne, ikke den præcise afstand.',
     'Videre til paratviden om regeringen.'),
    (5, 'Quiz 5 · paratviden', 'Regeringen og Folketinget', SPM_REGERING,
     'Ting man skal kunne uden at slå op. Tallene er fra valget 24. marts '
     '2026 og regeringen, der tiltrådte 3. juni 2026.',
     'Sidste runde: økonomi, EU og OECD.'),
    (6, 'Quiz 6 · økonomi', 'Økonomi, EU og OECD', SPM_OEKONOMI,
     'BNP, inflation, betalingsbalance og finanslov — og de to klubber, '
     'Danmark er med i.', None),
]
assert sum(1 for *_, slut in MODULER if slut is None) == 1, \
    'præcis én quiz skal være den sidste — den har id finalMsg'

OVERSIGT = f'''<section class="lesson" id="om">
<h2><span class="num">1</span> Sådan virker testen</h2>
<p class="sub">{ANTAL} spørgsmål fordelt på seks quizzer. Du får
svaret og en forklaring med det samme, du har trykket — så det er lige så
meget en træning som en prøve. Du kan tage den igen; den husker, hvor du
nåede til.</p>
<div class="box rule"><span class="rlabel">Hvad testen dækker</span><br>
<b>1. Teksterne</b> — lovprocessen og socialisering.<br>
<b>2. Digital socialisering</b> — tallene fra dataarket.<br>
<b>3. AI-ordbogen</b> — begreberne og de største aktører.<br>
<b>4. Partier og ideologi</b> — liberalisme, socialisme, konservatisme.<br>
<b>5. Regeringen og Folketinget</b> — paratviden.<br>
<b>6. Økonomi, EU og OECD</b> — BNP, inflation, betalingsbalance, finanslov.
</div>
<div class="box"><b>Tallene er slået op {OPDATERET}.</b> Mandatfordelingen
er fra valget 24. marts 2026, regeringen tiltrådte 3. juni 2026, og
inflationstallet er Danmarks Statistiks tal for oktober 2026. Et tal om
økonomi og politik har en holdbarhedsdato — står der det samme her om et
år, er siden forældet.</div>
<div class="figur">{F_SAL}<div class="figtekst">Folketinget efter valget.
Hvert punkt er ét mandat, og den stiplede streg ligger ved 90 — dér, hvor
flertallet begynder, talt fra venstre. Regeringens fire partier — S, SF,
M og RV — har tilsammen {REG_MANDATER} mandater, altså færre end de 90.
Derfor er det en mindretalsregering. Stregen skiller <b>ikke</b> regering
fra opposition: Enhedslisten og Alternativet ligger også til venstre for
den uden at sidde i regeringen.<br>
De fire grå mandater yderst til højre er Færøernes og Grønlands. De står
sidst, fordi de ikke hører hjemme på en dansk højre-venstre-akse — ikke
fordi de er et højrefløjsparti. To af dem støtter den nuværende
regering.</div></div>
</section>'''


def byg():
    s = open(SKABELON, encoding='utf-8').read()
    hoved = s[:s.index('<section class="lesson" id="beskriv">')]
    hale = s[s.index('<section class="lesson" id="results">'):]

    hoved = hoved.replace('<title>Statistik og sandsynlighed - 9. klasse</title>',
                          '<title>Samfundsfagstest · 60 spørgsmål - 9. klasse</title>')
    hoved = hoved.replace('321flyv · <span>Statistik</span>',
                          '321flyv · <span>Samfundsfagstest</span>')
    i = hoved.index('<nav class="jump">')
    j = hoved.index('</nav>', i)
    jump = ''.join(f'<a href="#quiz{nr}">{titel}</a> '
                   for nr, _, titel, *_ in MODULER)
    hoved = (hoved[:i] + '<nav class="jump"><a href="#om">Om testen</a> '
             + jump + '<a href="#results">Resultater</a> '
             '<a class="side" href="samfundsfag.html">Samfundsfag</a> '
             '<a class="side" href="index.html">Forside</a>' + hoved[j:])

    i = hoved.index('<section class="hero"')
    j = hoved.index('<button class="printbtn"', i)
    hoved = (hoved[:i] + '<section class="hero" id="intro">'
             '<span class="pill">9. klasse · samfundsfag</span>'
             f'<h1>Samfundsfagstest</h1><p><b>{ANTAL} spørgsmål</b> fra de opgivne '
             'tekster, AI-ordbogen og dataarket om digital socialisering — '
             'og om partier og ideologi, regeringen, EU og OECD, BNP, '
             'inflation, betalingsbalance og finanslov. Hvert spørgsmål har '
             'en figur, og svaret kommer med en forklaring med det samme.</p>'
             + hoved[j:])

    krop = OVERSIGT
    start = 1
    for nr, tag, titel, liste, undertitel, slut in MODULER:
        krop += quiz(nr, tag, titel, undertitel,
                     byg_spm(liste, start, ORDEN), len(liste), slut=slut)
        start += len(liste)
    assert start - 1 == ANTAL

    hale = hale.replace("var STORAGE_KEY = 'stat9_state_v1';",
                        "var STORAGE_KEY = 'samf9_test_v1';")
    navne = ','.join("'" + t + "'" for _, _, t, *_ in MODULER)
    hale = re.sub(r"var moduleNames = \[.*?\];",
                  f"var moduleNames = [{navne}];", hale, count=1, flags=re.S)
    # slutbeskeden i motoren taler om «den blandede quiz» — det hedder
    # sidste quiz ikke her
    gl_slut = "fm.textContent = 'Flot — alt rigtigt i den blandede quiz.';"
    assert hale.count(gl_slut) == 1
    hale = hale.replace(
        gl_slut, "fm.textContent = 'Flot — alt rigtigt i sidste runde.';")

    hale = hale.replace('Undervisningsmateriale til matematik i 9. klasse · '
                        'Statistik og sandsynlighed.',
                        'Undervisningsmateriale til samfundsfag i 9. klasse · '
                        f'Samfundsfagstest. Tallene er slået op {OPDATERET}.')

    ekstra = ('\n.qfig{margin:10px 0 12px}\n'
              '.qfig svg{width:100%;max-width:520px;height:auto;display:block;'
              'margin:0 auto}\n'
              '.box{background:var(--panel2);border:1px solid var(--line);'
              'border-radius:12px;padding:14px 18px;margin:14px 0;'
              'color:var(--muted);max-width:76ch}\n'
              '.box b{color:var(--ink)}\n'
              '.box.rule{border-left:5px solid var(--accent);background:#fff}\n'
              '.rlabel{font-size:.72rem;letter-spacing:.08em;'
              'text-transform:uppercase;color:var(--accent);font-weight:800}\n')
    hoved = hoved.replace('</style></head>', ekstra + '</style></head>', 1)
    return hoved + krop + hale


if __name__ == '__main__':
    doc = byg()
    open(UD, 'w', encoding='utf-8').write(doc)
    n = doc.count('<div class="q" ')
    assert n == ANTAL, f'{n} spørgsmål i filen, {ANTAL} forventet'
    assert doc.count('id="finalMsg"') == 1
    # quizmotorens kontrakt: lige mange quizzer og scoretavler uden for
    # <script> — i scriptet står der ét data-score til, som ikke tæller
    uden_script = re.sub(r'<script.*?</script>', '', doc, flags=re.S)
    assert uden_script.count('class="quiz"') == \
        uden_script.count('data-score') == len(MODULER)
    print(f'skrevet:  samfundsfagstest.html  ·  {n} spørgsmål i '
          f'{len(MODULER)} quizzer, {doc.count("<svg")} figurer, '
          f'{len(doc)//1024} kB')
