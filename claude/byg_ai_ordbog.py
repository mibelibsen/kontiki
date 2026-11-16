# -*- coding: utf-8 -*-
"""Bygger ai-ordbog.html - ordforklaring om AI og de to stoerste aktoerer.

**Tallene er slaaet op 15.11.2026, ikke husket.** De staar som konstanter
oeverst med kilde og dato, saa det kan ses, hvor gamle de er, og hvad der
er bekraeftet af en primaerkilde. Et tal om AI-brug er forael dt paa et
halvt aar - staar datoen ikke paa siden, bliver den usand uden at nogen
opdager det.

    python3 claude/byg_ai_ordbog.py
"""
import html
import os
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)
import figurer as FG

UD = os.path.join(ROD, 'ai-ordbog.html')
SKABELON = os.path.join(ROD, 'matematik.html')
OPDATERET = '15. november 2026'

# ---------------------------------------------------------------- tallene
# (vaerdi i millioner, enhed, hvornaar, hvor sikkert)
CHATGPT_BRUGERE = 900          # ugentlige
GEMINI_BRUGERE = 950           # maanedlige
AI_MODE_BRUGERE = 1000         # maanedlige, Google Soegning
OPENAI_EJERE = [('Ansatte og andre investorer', 47),
                ('Microsoft', 27), ('OpenAI Foundation', 26)]
assert sum(v for _, v in OPENAI_EJERE) == 100, 'ejerandelene skal give 100 %'

# ------------------------------------------------------------------ ordene
ORD = [
 ('Det grundlæggende', [
  ('Kunstig intelligens (AI)',
   'Computerprogrammer, der løser opgaver, man før troede krævede et '
   'menneske: genkende en stemme, skrive en tekst, finde en tumor på et '
   'røntgenbillede. Der er ingen bevidsthed indblandet.',
   'Forkortelsen kommer af engelsk <i>artificial intelligence</i>.'),
  ('Maskinlæring',
   'Den måde, de fleste AI-programmer bliver lavet på i dag: i stedet for '
   'at nogen skriver reglerne, får programmet enorme mængder eksempler og '
   'finder selv mønstrene.',
   'Ingen har skrevet reglen «en kat har knurhår». Programmet har set '
   'millioner af kattebilleder.'),
  ('Model',
   'Resultatet af træningen — selve filen med alt det, programmet har '
   'lært. Når nogen siger «en ny model», mener de en ny version, der er '
   'trænet forfra eller videre.', None),
  ('Træning',
   'Den proces, hvor modellen læser sine data igennem og justerer sig selv, '
   'til den gætter bedre. Det tager uger og koster millioner i strøm og '
   'computerkraft.', None),
  ('Parametre',
   'De tal inde i modellen, der bliver justeret under træningen. En stor '
   'model har hundredvis af milliarder parametre. Flere parametre er '
   'ikke '
   'automatisk bedre.', None),
  ('Træningsdata',
   'Det, modellen har læst eller set. For en sprogmodel typisk en meget '
   'stor del af det offentlige internet plus bøger og kode. Hvad der '
   'præcis er brugt, holder de fleste firmaer hemmeligt.',
   'Det er her striden om OPHAVSRET står.'),
  ('Neuralt netværk',
   'Den slags matematisk model, det hele bygger på. Navnet kommer af '
   'hjernens nerveceller, men ligheden er løs — det er lag af tal, der '
   'ganges sammen.', None),
  ('GPU og computerkraft',
   'GPU er det grafikkort, træningen kører på. «Compute» er branchens ord '
   'for, hvor meget regnekraft man har. Det er den knappe ressource, alle '
   'slås om. GPU står for Graphics Processing Unit.', None),
 ]),

 ('Sprogmodeller', [
  ('LLM (stor sprogmodel)',
   'En model, der er trænet til at gætte det næste stykke tekst. Det lyder '
   'småt, men gør du det godt nok og mange nok gange i træk, kan den svare '
   'på spørgsmål, oversætte og skrive kode.',
   'LLM er kort for <i>large language model</i>. ChatGPT, Gemini og Claude '
   'er alle sammen chatprogrammer oven på en LLM.'),
  ('Token',
   'Det stykke tekst som modellen regner i. Et token er typisk et kort '
   'ord eller en '
   'orddel. «Fyrtøjet» kan blive til to-tre tokens.',
   'Priser på AI opgøres i tokens, ikke i ord, og betales typisk efter '
   'antal millioner forbrugte tokens.'),
  ('Kontekstvindue',
   'Hvor meget modellen kan have for øje på én gang — din besked, '
   'samtalen indtil nu og de filer, du har vedlagt. Er vinduet fyldt, '
   'falder det ældste ud.',
   'Det er derfor en lang samtale kan «glemme» noget, du skrev i starten.'),
  ('Prompt',
   'Det, du skriver til modellen. En god prompt siger hvem der skriver, '
   'til hvem, hvad opgaven er, og hvordan svaret skal se ud.', None),
  ('Systemprompt',
   'En skjult instruktion, firmaet lægger ind før din. Den bestemmer '
   'tonen og grænserne. Du ser den ikke, men den er der.', None),
  ('Hallucination',
   'Når modellen finder på noget, der lyder rigtigt, men ikke er det — en '
   'kilde, der ikke findes, en lov, der ikke er vedtaget, et årstal, der '
   'er forkert.',
   '<b>Det vigtigste ord på hele listen.</b> Modellen gætter det næste '
   'ord; den slår ikke op. Tjek altid et tal, et navn og en kilde.'),
  ('Finjustering',
   'At træne en færdig model videre på et mindre, målrettet datasæt, så '
   'den bliver god til netop én ting — fx juridiske tekster eller en '
   'bestemt skrivestil.', None),
  ('RAG (opslag før svar)',
   'En metode, hvor programmet først slår op i en database eller på nettet '
   'og derefter lader modellen svare ud fra det, den fandt. Det gør '
   'hallucinationer sjældnere og giver kilder.',
   'Kort for <i>retrieval-augmented generation</i>.'),
  ('Multimodal',
   'En model, der kan andet end tekst: se billeder, høre lyd, se video. '
   'De fleste store modeller er multimodale i dag.', None),
  ('Benchmark',
   'En standardprøve, modeller måles på. Giv det ikke for meget vægt: en '
   'model kan være trænet på prøven og alligevel være ubrugelig til din '
   'opgave.', None),
 ]),

 ('Agentisk AI', [
  ('Agent',
   'Et AI-program, der ikke bare svarer, men <b>gør</b> noget: søger på '
   'nettet, skriver en fil, sender en mail, bestiller en vare. Det er '
   'modellen plus nogle værktøjer plus lov til at bruge dem.', None),
  ('Agentisk',
   'Tillægsordet. En agentisk opgave er en, hvor modellen selv vælger '
   'skridtene: «find ud af hvorfor regnearket ikke summerer, og ret det» '
   'i stedet for «hvad er 3 + 4?».',
   'Det er dét, der er nyt lige nu — og dét, der kan gå galt uden opsyn.'),
  ('Værktøjsbrug',
   'At modellen får lov at kalde rigtige funktioner: en lommeregner, en '
   'søgemaskine, et kalendersystem. Uden værktøjer kan den kun skrive '
   'tekst.', None),
  ('Løkke (agent-loop)',
   'Agenten arbejder i runder: tænk, brug et værktøj, se resultatet, tænk '
   'igen. Den stopper, når opgaven er løst — eller når den løber tør for '
   'penge eller tid.', None),
  ('Menneske i løkken',
   'At et menneske skal godkende, før agenten gør noget, der ikke kan '
   'fortrydes: sende, slette, betale.',
   'Den vigtigste sikring der findes. Spørg altid, hvem der godkender.'),
  ('MCP',
   'En fælles standard for, hvordan AI-programmer kobles til værktøjer og '
   'data. Som et USB-stik: samme stik til mange slags udstyr.',
   'Kort for <i>Model Context Protocol</i>.'),
  ('Autonomi',
   'Hvor langt agenten må gå alene. Der er stor forskel på «foreslå et '
   'svar» og «send svaret».', None),
 ]),

 ('AI i tingene omkring os', [
  ('IoT',
   'Internet of Things — tingenes internet. Alt det udstyr, der ikke er en '
   'computer, men alligevel er på nettet: varmetermostaten, '
   'højttaleren, elmåleren, e-cyklens lås.', None),
  ('IoT-AI',
   'AI, der kører i eller for den slags udstyr. Robotstøvsugeren, der '
   'genkender en sko. Varmepumpen, der lærer, hvornår I står op.', None),
  ('Edge AI',
   'AI, der kører <b>på selve enheden</b> i stedet for ude i et '
   'datacenter. Det er hurtigere, virker uden net, og dine data forlader '
   'ikke dimsen.',
   '«Edge» betyder kanten af nettet — altså ude hos dig.'),
  ('Sensor',
   'Det, der måler: mikrofon, kamera, termometer, bevægelsesmåler. En '
   'IoT-AI er aldrig bedre end sine sensorer.', None),
  ('Indlejret system',
   'En lille computer, der sidder inde i en ting og kun laver dét ene. '
   'Der er ofte en i din mikroovn.', None),
 ]),

 ('Billeder, lyd og video', [
  ('Generativ AI',
   'Fællesnavnet for AI, der laver noget nyt — tekst, billeder, lyd, video '
   '— frem for bare at sortere eller genkende.', None),
  ('Diffusionsmodel',
   'Den slags model, de fleste billedgeneratorer bruger. Den starter med '
   'ren støj og fjerner støjen lidt efter lidt, til der står et billede.',
   None),
  ('Deepfake',
   'En video eller lydoptagelse af en rigtig person, der siger eller gør '
   'noget, hun aldrig har sagt eller gjort.',
   'Teknikken er til at få fat i, og den bliver brugt til svindel og '
   'mobning. Tjek altid, hvor en video kommer fra.'),
  ('Stemmekloning',
   'At efterligne en bestemt persons stemme ud fra få sekunders lyd.',
   'Svindelnummeret «mor, jeg har mistet min telefon» findes nu med din '
   'rigtige stemme.'),
  ('Vandmærke og oprindelse',
   'Et skjult mærke eller en mærkat i filen, der fortæller, at den er '
   'lavet af en maskine, og hvilken. Det hjælper, men kan fjernes.',
   'Standarden hedder C2PA. Fravær af mærke beviser ingenting.'),
 ]),

 ('Det, man bør vide om', [
  ('Bias (skævhed)',
   'Modellen arver skævhederne i sine data. Er lægerne på billederne '
   'mest gamle, tegner den gamle læger.',
   'Det er ikke en fejl i koden. Det er et spejl af materialet.'),
  ('Ophavsret',
   'Modellerne er trænet på tekst og billeder, nogen har lavet og ejer. '
   'Om det er lovligt, er ikke afgjort — der kører retssager flere '
   'steder.', None),
  ('Persondata og GDPR',
   'Skriver du personfølsomme oplysninger ind i en chatbot, forlader de '
   'din computer. Skriv aldrig cpr-numre, karakterer eller andres '
   'genkendelige navne og sygdomme ind i et AI-program. Du må gerne '
   'bruge almindelige fornavne.', None),
  ('EU-forordningen om AI',
   'EU’s lov om kunstig intelligens. Den deler anvendelser op efter '
   'risiko: noget er forbudt, noget kræver tilladelse og mærkning, og '
   'resten er frit.', None),
  ('Energi og vand',
   'Træning og brug af store modeller kræver meget strøm, og '
   'datacentrene køles med vand. Det er en reel omkostning, også når '
   'svaret kommer gratis på skærmen.', None),
  ('Åben kilde mod lukket model',
   'Nogle firmaer udgiver modellens filer, så enhver kan køre den selv. '
   'Andre holder dem hemmelige og sælger adgang. Begge dele kaldes '
   'nogle gange «open source», og det er sjældent helt rigtigt.', None),
  ('Kildekritik',
   'Et AI-svar er ikke en kilde. Det er et gæt, der lyder godt. Spørg '
   'altid: '
   'hvor ved den det fra, og kan jeg finde det samme et andet sted?',
   '<b>Den vane, der betyder mest.</b>'),
  ('AGI',
   'Kunstig generel intelligens — en maskine, der kan alt det, et '
   'menneske kan. Den findes ikke, og der er ikke enighed om, hvornår '
   'eller om den kommer. Ordet bruges meget i markedsføring.', None),
  ('API',
   'Den dør, et program bruger til at tale med et andet. Når en app har '
   '«AI indbygget», er det som regel et kald til en stor models API.',
   None),
 ]),
]

NAV = {'Det grundlæggende': 'Grundbegreber',
       'Sprogmodeller': 'Sprogmodeller',
       'Agentisk AI': 'Agentisk AI',
       'AI i tingene omkring os': 'AI i ting og IoT',
       'Billeder, lyd og video': 'Billeder og lyd',
       'Det, man bør vide om': 'Det man bør vide'}
assert set(NAV) == {t for t, _ in ORD}, 'NAV og ORD skal have samme temaer'

ANTAL_ORD = sum(len(v) for _, v in ORD)
assert ANTAL_ORD >= 40, f'kun {ANTAL_ORD} ord'


# --------------------------------------------------------------- aktoererne
# Tal slaaet op 15.11.2026. 'kilde' siger, hvor sikkert tallet er, og det
# staar paa siden: et brugertal uden kilde er et rygte.
A = [
 dict(navn='OpenAI', produkt='ChatGPT',
      ejer='OpenAI Group PBC. Efter omlægningen i oktober 2025 ejer '
           '<b>OpenAI Foundation</b> — en fond uden ejere — ca. 26 %, '
           '<b>Microsoft</b> ca. 27 %, og ansatte og øvrige investorer ca. '
           '47 %. Fonden udpeger bestyrelsen og har dermed kontrollen, selv '
           'om Microsoft har den største enkeltandel.',
      brugere=f'ca. {CHATGPT_BRUGERE} mio. <b>om ugen</b>',
      tal=None, enhed='uge',
      brug='Skrive og omskrive tekst, svare på spørgsmål, programmere, '
           'oversætte, lave billeder, lektiehjælp. Et sted man går hen: '
           'en app og en hjemmeside.',
      saerligt='Først på markedet, og stadig det navn folk siger i stedet '
               'for «AI». Firmaet er ikke en almindelig virksomhed — en '
               'fond har kontrollen, og formålet står i vedtægterne.',
      kilde='OpenAI, februar 2026. Nyere tal på 1 og 1,2 mia. findes, men '
            'kun hos statistiksider, ikke hos OpenAI selv.'),

 dict(navn='Google', produkt='Gemini',
      ejer='<b>Alphabet Inc.</b> — en helt almindelig børsnoteret '
           'virksomhed. Hvem som helst kan købe en aktie.',
      brugere=f'{GEMINI_BRUGERE} mio. <b>om måneden</b> i appen',
      tal=GEMINI_BRUGERE, enhed='måned',
      brug='Svarene øverst i en Google-søgning, hjælp i Gmail og Docs, '
           'assistenten i Android-telefoner — og appen. Mange bruger den '
           'uden at have valgt den.',
      saerligt='Distributionen. Google skal ikke have folk til at gå et nyt '
               'sted hen; de er der i forvejen. Google laver også sine egne '
               'chips, så de ikke skal købe regnekraft af andre.',
      kilde='Alphabets regnskab for 2. kvartal 2026, bekræftet i selskabets '
            'indberetning til det amerikanske børstilsyn. Dertil over 1 mia. '
            'om måneden i AI-tilstanden i Google Søgning.'),

 dict(navn='Meta', produkt='Meta AI og Llama',
      ejer='<b>Meta Platforms</b>, børsnoteret, men Mark Zuckerberg har '
           'aktier med ekstra stemmeret og bestemmer dermed alene.',
      brugere='ca. 1.000 mio. <b>om måneden</b>',
      tal=1000, enhed='måned',
      brug='Ligger inde i Facebook, Instagram og WhatsApp. Llama-modellerne '
           'hentes og bruges af andre firmaer og forskere.',
      saerligt='Meta har udgivet sine modeller, så andre kan hente dem og '
               'køre dem selv. Brugertallet skal læses med forsigtighed: de '
               'fleste har ikke valgt Meta AI, den kom med appen.',
      kilde='Zuckerberg, maj 2025 — det er det nyeste tal, Meta selv har '
            'sagt. Højere tal (1,2 og 1,5 mia.) står kun på blogs, der '
            'modsiger hinanden.'),

 dict(navn='Microsoft', produkt='Copilot',
      ejer='<b>Microsoft</b>, børsnoteret. Ejer samtidig ca. 27 % af OpenAI '
           'og bruger OpenAIs modeller i sine egne produkter.',
      brugere='ca. 150 mio. <b>om måneden</b>',
      tal=150, enhed='måned',
      brug='Windows, Word, Excel, Outlook, Teams — og programmering i '
           'GitHub Copilot. Mest på arbejdspladser; Microsoft sælger '
           'adgangen pr. ansat.',
      saerligt='Tjener penge på AI uden selv at skulle lave den bedste '
               'model: de lejer OpenAIs og lægger den ind i programmer, '
               'firmaer allerede betaler for.',
      kilde='Microsofts kvartalsregnskaber, 2026. Firmaet oplyser også '
            '~900 mio. om måneden, der bruger «AI-funktioner» — en meget '
            'bredere og løsere definition.'),

 dict(navn='Anthropic', produkt='Claude',
      ejer='<b>Anthropic PBC</b>. Ikke børsnoteret. Google og Amazon har '
           'investeret store beløb, men ingen af dem har kontrollen; den '
           'ligger hos stifterne og en særlig fond (The Long-Term Benefit '
           'Trust), der kan udpege bestyrelsesmedlemmer.',
      brugere='oplyses ikke',
      tal=None, enhed=None,
      brug='Mest i virksomheder og til programmering. Over halvdelen af '
           'omsætningen kommer fra erhvervskunder.',
      saerligt='Få private brugere, men meget stor hos virksomheder — ca. '
               '80 % af omsætningen er erhverv. Firmaet blev stiftet af '
               'folk, der forlod OpenAI, og profilerer sig på sikkerhed.',
      kilde='Anthropic offentliggør ikke brugertal. Oplysningerne om '
            'omsætning er pressens tal, ikke reviderede regnskaber.'),

 dict(navn='ByteDance', produkt='Doubao (豆包)',
      ejer='<b>ByteDance</b>, kinesisk, ikke børsnoteret. Samme firma, der '
           'ejer TikTok.',
      brugere='382 mio. <b>om måneden</b> i Kina',
      tal=382, enhed='måned',
      brug='Kinas mest brugte chatbot: lektiehjælp, oversættelse, '
           'billeder, stemme. Ligger inde i ByteDances egne apps.',
      saerligt='Større end alle andre kinesiske chatbots tilsammen og '
               'næsten ukendt i Europa. Et godt bevis på, at «de største» '
               'afhænger af, hvor man måler.',
      kilde='QuestMobile, juni 2026. Måler kun mobilbrug i Kina.'),

 dict(navn='Alibaba', produkt='Qwen (Tongyi)',
      ejer='<b>Alibaba Group</b>, kinesisk, børsnoteret i Hongkong og '
           'New York.',
      brugere='167 mio. <b>om måneden</b> i Kina',
      tal=167, enhed='måned',
      brug='Chatbot og modeller, andre bygger videre på. Qwen er en af de '
           'mest hentede åbne modeller i verden.',
      saerligt='Alibaba udgiver modellernes filer, så enhver kan køre dem '
               'selv. Firmaet har brugt milliarder på rabatkuponer for at '
               'få brugere over i appen.',
      kilde='QuestMobile, juni 2026. Måler kun mobilbrug i Kina.'),

 dict(navn='DeepSeek', produkt='DeepSeek',
      ejer='<b>DeepSeek</b> i Hangzhou, ejet af den kinesiske '
           'investeringsfond <b>High-Flyer</b>. Ikke børsnoteret.',
      brugere='ca. 130 mio. <b>om måneden</b> i Kina',
      tal=130, enhed='måned',
      brug='Chat og programmering. Modellen hentes og køres af firmaer og '
           'forskere i hele verden, også uden for Kina.',
      saerligt='I januar 2025 viste DeepSeek, at man kunne lave en model '
               'næsten lige så god som de dyreste — for en brøkdel af '
               'pengene. Aktiekurserne faldt verden over på én dag. '
               'Brugertallet er siden faldet.',
      kilde='QuestMobile, juni 2026. Måler kun mobilbrug i Kina.'),

 dict(navn='SpaceX', produkt='Grok (tidligere xAI)',
      ejer='<b>SpaceX</b>. Elon Musks AI-firma xAI blev 2. februar 2026 '
           'købt af SpaceX og er nu en del af det. Samme mand ejer også X '
           '(tidligere Twitter), hvor Grok ligger indbygget.',
      brugere='ca. 117 mio. <b>om måneden</b>',
      tal=117, enhed='måned',
      brug='Chat inde i X, billeder og video. Bruges også som det '
           'frække alternativ: Grok har færre spærringer end de andre.',
      saerligt='Det eneste af de store, der er bygget oven på et socialt '
               'medie, og det, der har haft flest sager om, hvad en '
               'chatbot må sige og vise.',
      kilde='SpaceX’ børsprospekt, marts 2026. Tallet dækker dem, der '
            'bruger Grok-funktioner i X — ikke kun appen.'),

 dict(navn='Nvidia', produkt='chips til AI',
      ejer='<b>Nvidia</b>, børsnoteret i USA. Verdens mest værdifulde '
           'selskab i perioder af 2025 og 2026.',
      brugere='ikke en chatbot — men ca. 80–90 % af markedet for AI-chips',
      tal=None, enhed=None,
      brug='Alle de andre på denne liste køber eller lejer Nvidias chips '
           'for at kunne træne og køre deres modeller.',
      saerligt='Den vigtigste aktør, som ingen elever bruger direkte. '
               'Nvidia sælger ikke AI; de sælger det, AI kører på. Derfor '
               'tjener de penge, uanset hvem der vinder kampen om '
               'brugerne.',
      kilde='IDC m.fl., 2026. Vurderingerne går fra 75 % til 92 % — det '
            'afhænger af, om man måler alle AI-chips eller kun '
            'grafikkort til datacentre.'),
]
assert len(A) == 10, f'der skal være ti aktører, der er {len(A)}'
# chipmarkedet: Nvidia, AMD, resten (IDC's tal for 2026)
CHIP = [('Nvidia', 81), ('AMD', 10), ('Alle andre', 9)]
assert sum(v for _, v in CHIP) == 100

# soejlerne navngives efter produktet, ikke firmaet: det er Gemini og Grok,
# ungerne kender, og en blanding af firma- og produktnavne paa samme akse er
# i sig selv vildledende.
KORT = {'Google': 'Gemini', 'Meta': 'Meta AI', 'Microsoft': 'Copilot',
        'ByteDance': 'Doubao', 'Alibaba': 'Qwen', 'SpaceX': 'Grok',
        'DeepSeek': 'DeepSeek'}
MND = [(KORT[a['navn']], a['tal']) for a in A if a['enhed'] == 'måned']
MND = sorted(MND, key=lambda t: -t[1])
assert len(MND) == 7 and all(v for _, v in MND)


# ----------------------------------------------------------------- figurer
def trin(overskrift, under, gruppe, W=640):
    """Et trin til procesdiagrammet, med bredden regnet efter.

    procesdiagram ombryder ikke: en for lang undertekst loeber ud over
    kassens hoejre kant og bliver klippet. Teksten saettes i monospace med
    font-size 10.5, hvor hvert tegn fylder 0,6 em, og den begynder 46 px
    inde i en kasse, der er W-20 bred. Saa her er pladsen regnet ud i
    stedet for maalt paa oejemaal.
    """
    plads = int(((W - 20) - 46 - 12) / (10.5 * 0.6))
    assert len(under) <= plads, \
        f'underteksten til «{overskrift}» er {len(under)} tegn, der er plads til {plads}'
    return (overskrift, under, gruppe)


FIG_LLM = FG.procesdiagram([
 trin('Du skriver', 'Din tekst deles i tokens, dvs. små stykker ord.',
      'ind'),
 trin('Modellen regner',
      'Den regner ud, hvilket token der er mest sandsynligt som det næste.',
      'kerne'),
 trin('Ét token ad gangen',
      'Den skriver det, lægger det til teksten og regner forfra.', 'kerne'),
 trin('Og igen', 'Token for token, til svaret er færdigt.', 'kerne'),
 trin('Du læser et svar',
      'Det ser ud, som om nogen har tænkt. Men i virkeligheden er det '
      'beregnet.', 'ud'),
], farver={'ind': FG.MUT, 'kerne': FG.BLA, 'ud': FG.GRO})

FIG_AGENT = FG.procesdiagram([
 trin('Mål', 'Du giver en opgave, ikke et spørgsmål: «find fejlen og ret den».',
      'ind'),
 trin('Tænk', 'Modellen vælger selv næste skridt.', 'kerne'),
 trin('Brug et værktøj', 'Søg, læs en fil, kør en beregning, send noget.',
      'kerne'),
 trin('Se resultatet', 'Virkede det? Hvis nej: tilbage til «tænk».', 'kerne'),
 trin('Menneske i løkken',
      'Nogen godkender, før agenten gør noget, der ikke kan fortrydes.',
      'stop'),
], farver={'ind': FG.MUT, 'kerne': FG.BLA, 'stop': FG.ROD},
   legende=[('Disse tre gentages, til opgaven er løst', 'kerne'),
            ('Spærringen', 'stop')])

FIG_MND = FG.soejler([v for _, v in MND], [n for n, _ in MND],
                     titel='Brugere om måneden — kun dem, der måles i måneder',
                     ynavn='millioner', W=720, H=330)

FIG_CHIP = FG.cirkeldiagram(CHIP)
FIG_EJERE = FG.cirkeldiagram(OPENAI_EJERE)

# ------------------------------------------------------------------- siden
def ord_html():
    ud = ''
    for i, (tema, poster) in enumerate(ORD, 1):
        ud += (f'<section class="lesson" id="tema{i}">'
               f'<h2><span class="num">{i}</span> {html.escape(tema)}</h2>'
               f'<dl class="ordliste">')
        for ord, forklaring, eks in poster:
            ud += (f'<dt>{html.escape(ord)}</dt><dd>{forklaring}'
                   + (f'<span class="eks">{eks}</span>' if eks else '')
                   + '</dd>')
        ud += '</dl></section>'
    return ud


def aktoer_html():
    """Ét kort pr. aktør. Felterne er de fire, der blev spurgt om:
    ejer, brugere, hvad det bruges til, og hvad der er særligt."""
    ud = ''
    for i, a in enumerate(A, 1):
        ud += (f'<div class="akt"><h3><span class="rang">{i}</span>'
               f'{a["navn"]} <span class="pro">· {a["produkt"]}</span></h3>'
               f'<dl><dt>Hvem ejer det</dt><dd>{a["ejer"]}</dd>'
               f'<dt>Brugere</dt><dd>{a["brugere"]}'
               f'<span class="eks">{a["kilde"]}</span></dd>'
               f'<dt>Bruges mest til</dt><dd>{a["brug"]}</dd>'
               f'<dt>Det særlige</dt><dd>{a["saerligt"]}</dd></dl></div>')
    return ud


def tabel_html():
    r = ''
    for i, a in enumerate(A, 1):
        r += (f'<tr><td class="r">{i}</td><td><b>{a["navn"]}</b></td>'
              f'<td>{a["produkt"]}</td><td>{a["brugere"]}</td></tr>')
    return ('<table class="ovb"><thead><tr><th class="r">#</th><th>Aktør</th>'
            '<th>Produkt</th><th>Brugere</th></tr></thead><tbody>'
            + r + '</tbody></table>')


AKTOERER = f'''<section class="lesson" id="aktoerer">
<h2><span class="num">{len(ORD) + 1}</span> De ti største aktører</h2>
<p class="sub">Her er de ti, der betyder mest lige nu — med de tal, der
faktisk kan dokumenteres, og en note om, hvor hvert tal kommer fra.</p>

{tabel_html()}

<div class="box"><b>Pas på enhederne.</b> OpenAI opgør sine brugere
<i>pr. uge</i>. Alle de andre opgør <i>pr. måned</i>. De tal kan derfor
ikke sammenlignes direkte, selv om de står lige under hinanden i tabellen
og ligner hinanden. Og de kinesiske tal dækker kun mobilbrug i Kina.
Det er præcis den slags, I har lært at fange i modulet om manipulation.</div>

<div class="figur">{FIG_MND}<div class="figtekst">Kun de syv, der tælles
pr. måned, er med her — ChatGPT, Claude og Nvidia kan ikke sættes ind på
samme akse, fordi de ikke måler det samme. Selv blandt de syv er det ikke
helt ens: Meta AI og Copilot følger med apps og programmer, folk har i
forvejen, mens Gemini-tallet er dem, der åbner selve appen.</div></div>

{aktoer_html()}

<div class="box"><b>Og de andre?</b> <b>Mistral</b> i Frankrig er Europas
største bud — den hollandske chipmaskineproducent ASML er største
aktionær, og modellerne kan hentes og køres på egne computere, hvilket
gør dem interessante for europæiske myndigheder og skoler.
<b>Apple</b> lægger AI ind i iPhonen, <b>Amazon</b> sælger regnekraften,
og <b>Baidu</b> og <b>Tencent</b> er store i Kina.</div>

<h3>Den vigtigste aktør er den, ingen bruger</h3>
<p class="sub">Nvidia laver ikke en chatbot. De laver de chips, alle de
andre er nødt til at købe. Derfor tjener de penge, uanset hvem der vinder
kampen om brugerne.</p>
<div class="figur cirk">{FIG_CHIP}<div class="figtekst">Markedet for AI-chips
til datacentre. Vurderingerne går fra 75 % til 92 % til Nvidia alt efter,
hvad man tæller med — her er IDC's tal for 2026. Et marked, hvor én
sælger har fire femtedele, kaldes et monopol i alt andet end firmaets navn.
</div></div>

<h3>Hvem bestemmer i OpenAI?</h3>
<div class="figur cirk">{FIG_EJERE}<div class="figtekst">Ejerandelene i OpenAI
Group PBC efter omlægningen i oktober 2025. Bemærk, at den, der ejer mest,
ikke er den, der bestemmer: fonden ejer ca. 26 % og udpeger
bestyrelsen.</div></div>

<div class="box rule"><span class="rlabel">Sådan læser du et brugertal</span>
<br><b>1.</b> Hvilken enhed? Uge, måned, dag — eller «konti oprettet»?<br>
<b>2.</b> Hvornår er det målt? Et halvt år gammelt tal er gammelt her.<br>
<b>3.</b> Hvem har talt? Firmaet selv, en myndighed, eller en blog, der
skriver af efter en anden blog?<br>
<b>4.</b> Har brugeren valgt det? Et tal, der tæller alle, som fik AI
med i en app de allerede havde, er ikke det samme som et tal, der tæller
dem, der selv gik derhen.</div>
</section>'''
def byg():
    s = open(SKABELON, encoding='utf-8').read()
    css = s[s.index('<style>') + 7:s.index('</style>')]
    css += '''
nav.jump{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
nav.jump a{color:var(--muted);text-decoration:none;font-size:.86rem;
padding:6px 11px;border-radius:999px;border:1px solid transparent;
transition:.15s;display:inline-flex;align-items:center;min-height:40px}
nav.jump a:hover{color:var(--ink);border-color:var(--line);
background:var(--panel2)}
nav.jump a.side{border-color:var(--line);background:var(--panel2);
color:var(--ink);font-weight:600}
@media(max-width:760px){header.top nav.jump{width:100%;margin-left:0;gap:4px}
header.top nav.jump a{padding:5px 9px;font-size:.8rem}}
.lesson{background:#fff;border:1px solid var(--line);border-radius:14px;
padding:20px 24px;margin:16px 0}
.lesson h2{font-size:1.3rem;margin:0 0 6px;display:flex;align-items:center;
gap:12px}
.lesson h3{font-size:1.08rem;margin:22px 0 8px}
.lesson .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.lesson .sub{color:var(--muted);margin:0 0 10px;max-width:72ch}
dl.ordliste{margin:10px 0 0}
dl.ordliste dt{font-weight:700;margin:16px 0 2px;color:var(--ink)}
dl.ordliste dd{margin:0;color:var(--muted);max-width:72ch}
dl.ordliste dd b{color:var(--ink)}
dl.ordliste .eks{display:block;margin-top:5px;padding-left:12px;
border-left:3px solid var(--line);font-size:.93rem}
.box{background:var(--panel2);border:1px solid var(--line);
border-radius:12px;padding:14px 18px;margin:14px 0;color:var(--muted);
max-width:76ch}
.box b{color:var(--ink)}
.box.rule{border-left:5px solid var(--accent);background:#fff}
.rlabel{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;
color:var(--accent);font-weight:800}
.figur{margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figur.cirk svg{max-width:520px}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;
text-align:left;max-width:68ch;margin-left:auto;margin-right:auto}
table.krit{width:100%;border-collapse:collapse;margin:10px 0;
font-size:.95rem}
table.krit th,table.krit td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.krit th{background:var(--panel2);width:26%;color:var(--ink)}
table.krit td{color:var(--muted)}
table.krit td b{color:var(--ink)}
@media(max-width:600px){table.krit th{width:34%}}
.akt{border:1px solid var(--line);border-left:5px solid var(--accent);
border-radius:12px;padding:4px 20px 16px;margin:16px 0;background:#fff}
.akt h3{display:flex;align-items:center;gap:10px;margin:16px 0 4px}
.akt .rang{width:26px;height:26px;border-radius:8px;display:grid;
place-items:center;font-size:.85rem;font-weight:800;background:var(--panel2);
color:var(--accent);border:1px solid var(--line);flex:0 0 auto}
.akt .pro{font-weight:400;color:var(--muted);font-size:.95rem}
.akt dl{margin:6px 0 0;display:grid;grid-template-columns:140px 1fr;
gap:4px 16px}
.akt dt{font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;
color:var(--accent);font-weight:800;padding-top:3px}
.akt dd{margin:0;color:var(--muted);max-width:70ch}
.akt dd b{color:var(--ink)}
.akt .eks{display:block;margin-top:4px;font-size:.85rem;font-style:italic}
@media(max-width:620px){.akt dl{grid-template-columns:1fr;gap:0}
.akt dt{margin-top:12px}}
table.ovb{width:100%;border-collapse:collapse;margin:14px 0;font-size:.93rem}
table.ovb th,table.ovb td{border-bottom:1px solid var(--line);
padding:8px 10px;text-align:left}
table.ovb thead th{background:var(--panel2);font-size:.78rem;
letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
table.ovb td{color:var(--muted)}
table.ovb td b{color:var(--ink)}
table.ovb .r{width:2.4em;text-align:right;color:var(--muted)}
@media print{.akt,.ovb tr{break-inside:avoid}}
@media print{header.top,.printbtn{display:none!important}
.lesson,.figur,table.krit{break-inside:avoid}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''
    jump = ''.join(f'<a href="#tema{i}">{html.escape(NAV[t])}</a>'
                   for i, (t, _) in enumerate(ORD, 1))
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>AI-ordbog · 9. klasse</title><style>' + css
            + '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="index.html">321flyv · <span>AI-ordbog</span>'
            '</a><nav class="jump">' + jump
            + '<a href="#aktoerer">De ti største</a>'
            '<a class="side" href="index.html">Forside</a>'
            '</nav></div></header><main>'
            '<section class="hero"><span class="pill">9. klasse · '
            'projektviden</span><h1>AI-ordbog</h1>'
            f'<p>{ANTAL_ORD} ord og begreber, man støder på, når der er tale '
            'om kunstig intelligens — fra <i>agentisk</i> over <i>LLM</i> til '
            '<i>IoT-AI</i>. Hvert ord er forklaret på dansk og uden '
            'forudsætninger. Til sidst de ti største aktører: hvem der ejer dem, '
            'hvor mange der bruger dem, og hvad de bruges til.</p>'
            '<button class="printbtn" onclick="window.print()">Print siden'
            '</button></section>'
            f'<div class="box"><b>Tallene i sidste afsnit er slået op '
            f'{OPDATERET}.</b> Brugertal for AI ændrer sig hurtigt, og et tal '
            'uden dato er ubrugeligt.</div>'
            '<div class="figur">' + FIG_LLM + '<div class="figtekst">'
            'Sådan arbejder en sprogmodel. Den slår ikke op og den tænker '
            'ikke efter; den regner ud, hvad der er mest sandsynligt som det '
            'næste. Det er hele forklaringen på, hvorfor den kan tage fejl '
            'med fuld overbevisning.</div></div>'
            + ord_html()
            + '<div class="figur">' + FIG_AGENT + '<div class="figtekst">'
            'Forskellen på en chatbot og en agent: agenten får lov at handle, '
            'og den bliver ved, til opgaven er løst.</div></div>'
            + AKTOERER
            + '</main><footer>Projektmateriale · 9. klasse · '
            f'AI-ordbog. Tallene er slået op {OPDATERET}.</footer>'
            '</body></html>')


if __name__ == '__main__':
    doc = byg()
    open(UD, 'w', encoding='utf-8').write(doc)
    print(f'skrevet:  ai-ordbog.html  ·  {ANTAL_ORD} ord i '
          f'{len(ORD)} temaer, {doc.count("<svg")} figurer')
