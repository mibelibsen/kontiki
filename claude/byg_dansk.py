# -*- coding: utf-8 -*-
"""Bygger dansk-siderne — skriftlig fremstilling i 9. klasse.

    /dansk            oversigt over sættene
    /dansk/saet-1     øvelsessæt 1
    /dansk/saet-2     øvelsessæt 2
    /dansk/saet-3     øvelsessæt 3
    /dansk/essay      genrevejledning til essayet

Adresserne staar som omskrivninger i vercel.json; filerne hedder
dansk.html og dansk-saet-1.html og saa videre i roden.

Siderne er **ulistede med vilje**: ingen anden side paa sitet linker til
dem, og de har noindex. Ulistet er ikke det samme som privat - har man
adressen, kan man laese dem.

Saet 1 og 2 er brugerens egne, hentet fra mibelib-space.vercel.app/dansk.
Saet 3 er skrevet herfra over de tre emner, brugeren bad om. Hver side er
selvbaerende: CSS'en staar inline, intet hentes fra roden.

    python3 claude/byg_dansk.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

ROD = ''
SIDER = {'saet-1': 'Sæt 1', 'saet-2': 'Sæt 2', 'saet-3': 'Sæt 3',
         'essay': 'Essay'}


def fil(noegle):
    """Filnavnet i roden for en adresse under /dansk."""
    return 'dansk.html' if noegle is None else f'dansk-{noegle}.html'


# ---------------------------------------------------------------- forlæg
def citater(indledning, stykker, note):
    s = f'<p class="forlaeg-ind">{html.escape(indledning)}</p><div class="cit">'
    for tekst, hvem in stykker:
        s += (f'<blockquote>{html.escape(tekst)}'
              f'<cite>{html.escape(hvem)}</cite></blockquote>')
    return s + f'</div><p class="konstrueret">{html.escape(note)}</p>'


def opslag(overskrift, krop, note):
    return (f'<div class="opslag"><h5>{html.escape(overskrift)}</h5>'
            f'<p>{html.escape(krop)}</p></div>'
            f'<p class="konstrueret">{html.escape(note)}</p>')


def remse(indledning, dele, note):
    return (f'<p class="forlaeg-ind">{html.escape(indledning)}</p>'
            f'<p class="remse">'
            + ' · '.join(html.escape(d) for d in dele)
            + f'</p><p class="konstrueret">{html.escape(note)}</p>')


def program(indledning, linjer, note):
    s = f'<p class="forlaeg-ind">{html.escape(indledning)}</p><ul class="prog">'
    for tid, hvad, frem in linjer:
        s += (f'<li><span class="tid">{html.escape(tid)}</span>'
              + (f'<b>{html.escape(hvad)}</b>' if frem else html.escape(hvad))
              + '</li>')
    return s + f'</ul><p class="konstrueret">{html.escape(note)}</p>'


# --------------------------------------------------------------- sættene
# (nr, titel, genre, [kilder], forlaeg, situation, rolle, opgavetitel,
#  forberedelse, [(udsagnsord, resten)])
SAET = {}

SAET['saet-1'] = dict(
    maerke='Sæt 1',
    kort='Den mobilfri skole, madspild, et sted at være for byens unge og '
         'en anmeldelse til skolebladet. Tre af opgaverne har kilder fra '
         'dr.dk.',
    genrer=['debatindlæg', 'mundtligt oplæg', 'henvendelse', 'anmeldelse'],
    opgaver=[
 dict(titel='Virker den mobilfri skole?', genre='Debatindlæg til en avis',
      kilder=[('https://www.dr.dk/nyheder/indland/flere-skoler-har-allerede-mobilfri-skoletid-og-det-er-de-glade',
               'Flere skoler har allerede mobilfri skoletid — og det er de glade for',
               'Videoklip fra en skole, der har haft mobilfri skoletid i flere år.'),
              ('https://www.dr.dk/nyheder/indland/forsker-mobilforbud-i-skolen-kommer-ti-aar-sent-nu-ligger-problemet-et-andet-sted',
               'Forsker: Mobilforbud i skolen kommer ti år for sent',
               'En forsker mener ikke, at reglerne ændrer så meget.')],
      forlaeg=citater(
        'Fire unge fortæller om deres første tid med den mobilfri skoledag:',
        [('Frikvartererne blev pludselig larmende. Vi snakkede faktisk med '
          'hinanden igen.', 'Alma, 15 år'),
         ('Jeg brugte min telefon til ordbog, kalender og billeder af '
          'tavlen. Det rammer reglerne også.', 'Yusuf, 15 år'),
         ('Man lærer jo ikke at styre den ved at få den taget fra sig. Man '
          'lærer det ved at øve sig.', 'Silje, 16 år'),
         ('Jeg kan bedre koncentrere mig nu. Men jeg savner at kunne skrive '
          'hjem i pausen.', 'Oskar, 14 år')],
        'Udsagnene er konstrueret til dette øvelsessæt.'),
      situation='Fra dette skoleår skal folkeskoler og fritidstilbud være '
        'mobilfri. Beslutningen er truffet i Folketinget, og den enkelte '
        'skole laver sin egen lokale politik. Nu er det jer, der mærker, '
        'hvad reglerne betyder i praksis — og I bliver ikke altid spurgt.',
      rolle='Du vælger at skrive et debatindlæg til en avis om, hvordan den '
        'mobilfri skoledag fungerer.',
      opgavetitel='Skriv et debatindlæg til en avis',
      forberedelse='Som forberedelse skal du se og læse kilderne ovenfor og '
        'søge mere viden om emnet.',
      indled='I din tekst skal du:',
      krav=[('fortælle', 'om en konkret situation fra din egen skoledag, '
             'efter mobilerne blev lagt væk'),
            ('præsentere og kommentere', 'de vigtigste argumenter for og '
             'imod, som de kommer frem i kilderne'),
            ('argumentere', 'for, om reglerne virker efter hensigten'),
            ('foreslå', 'hvad der eventuelt skal laves om.')]),

 dict(titel='Maden, vi smider ud',
      genre='Mundtligt oplæg for 6.- og 7.-klasserne',
      kilder=[('https://www.dr.dk/nyheder/indland/salg-af-madspildsposer-slaar-rekord-herhjemme',
               'Salg af madspildsposer slår rekord herhjemme',
               'Om hvorfor flere og flere køber mad, der ellers ville blive '
               'smidt ud.')],
      forlaeg=remse(
        'Fra en klasses optælling af skraldespanden efter en frokostpause:',
        ['halve rugbrødsmadder', 'en uåbnet yoghurt',
         'tre bananer med brune pletter', 'en pose gulerødder', 'to boller',
         'rester af pastasalat'],
        'Eksemplet er konstrueret til dette øvelsessæt.'),
      situation='Meget af den mad, der bliver smidt ud, kunne sagtens være '
        'blevet spist. Det sker i køkkenet derhjemme, i kantinen og i '
        'madpakken. Nogle synes, det er et stort problem. Andre tænker slet '
        'ikke over det.',
      rolle='På skolen har I en temauge om mad. Du har sagt ja til at holde '
        'et mundtligt oplæg for skolens 6.- og 7.-klasser om madspild i '
        'hverdagen.',
      opgavetitel='Skriv teksten til dit mundtlige oplæg',
      forberedelse='Som forberedelse skal du søge viden om madspild og '
        'inddrage det i dit oplæg.',
      indled='I dit oplæg skal du:',
      krav=[('forklare', 'hvad madspild er, og hvorfor det betyder noget'),
            ('fortælle', 'om, hvad du selv har lagt mærke til derhjemme '
             'eller på skolen'),
            ('reflektere', 'over, hvad man kan gøre ved det, uden at det '
             'bliver besværligt'),
            ('afslutte', 'med en opfordring, som målgruppen kan gå hjem og '
             'bruge.')]),

 dict(titel='Et sted at være',
      genre='Henvendelse til kultur- og fritidsudvalget',
      kilder=[('https://www.dr.dk/nyheder/kultur/reels/massiv-tilslutning-til-ungdomsinitiativ',
               'Massiv tilslutning til ungdomsinitiativ',
               'Kort videoklip om en kommune, der har åbnet en klub igen '
               'efter syv år uden.')],
      forlaeg=opslag(
        'Har du en idé til unge i kommunen?',
        'Kultur- og fritidsudvalget har penge til ét nyt tilbud til unge '
        'mellem 13 og 18 år. Vi vil gerne høre fra jer, inden vi bestemmer '
        'os. Skriv til udvalget og fortæl, hvad der mangler dér, hvor I bor.',
        'Opslaget er konstrueret til dette øvelsessæt.'),
      situation='Nogle steder er der en hal, en klub eller et værested. '
        'Andre steder mødes man på en bænk, i en carport eller slet ikke. '
        'Hvor mødes I, hvor du bor — og hvad mangler der?',
      rolle='Du skriver en henvendelse til kultur- og fritidsudvalget, hvor '
        'du foreslår, hvad pengene skal bruges til.',
      opgavetitel='Skriv en henvendelse til udvalget',
      forberedelse='Som forberedelse skal du undersøge, hvilke tilbud der '
        'allerede findes, hvor du bor.',
      indled='I din tekst skal du:',
      krav=[('præsentere', 'dig selv og fortælle, hvem du skriver på vegne af'),
            ('beskrive', 'hvordan det ser ud i dag for unge, hvor du bor'),
            ('argumentere', 'for dit forslag, så udvalget kan se, hvorfor '
             'netop det skal vælges'),
            ('reflektere', 'over, hvad forslaget vil betyde for jer på '
             'længere sigt.')]),

 dict(titel='Anmeldelse til skolebladet',
      genre='Anmeldelse af en serie, en film, en bog, en podcast eller et spil',
      kilder=[],
      forlaeg=opslag(
        'Siden „Anbefalet af os“ mangler stof.',
        'Vi søger anmeldelser af serier, film, bøger, podcasts og spil. '
        'Skriv til dem, der ikke kender værket i forvejen — og afslør ikke '
        'slutningen.',
        'Opslaget er konstrueret til dette øvelsessæt.'),
      situation='Man bliver hurtigt enige om, at noget er godt eller '
        'dårligt. Sværere er det at forklare hvorfor, så andre kan bruge '
        'det til noget.',
      rolle='Du skriver en anmeldelse til skolebladet af en serie, en film, '
        'en bog, en podcast eller et spil, du kender godt.',
      opgavetitel='Skriv en anmeldelse til skolebladet',
      forberedelse='Som forberedelse skal du vælge det værk, du vil '
        'anmelde, og finde konkrete eksempler fra det.',
      indled='I din tekst skal du:',
      krav=[('præsentere', 'værket kort: titel, genre og hvem der står bag'),
            ('beskrive', 'handlingen eller indholdet uden at afsløre '
             'slutningen'),
            ('vurdere og begrunde', 'din vurdering med eksempler'),
            ('anbefale', 'værket til en bestemt målgruppe, og giv din '
             'anmeldelse en overskrift.')]),
    ])

SAET['saet-2'] = dict(
    maerke='Sæt 2',
    kort='Talen til afslutningen, AI-billeder og hvad man kan tro på, en '
         'ansøgning som frivillig og en fortælling om det, der ikke blev '
         'sagt.',
    genrer=['tale', 'guide', 'ansøgning', 'fortælling'],
    opgaver=[
 dict(titel='Sidste skoledag', genre='Tale til afslutningen', kilder=[],
      forlaeg=program('Programmet for afslutningen — udklip:',
        [('15.00', 'Velkomst ved Kaptajn/Skoleleder', False),
         ('15.15', 'Musik — 8. klasse', False),
         ('15.30', 'Tale ved en af de unge fra 9. klasse (5 minutter)', True),
         ('15.45', 'Uddeling af beviser', False),
         ('16.00', 'Kaffe og kage på broen', False)],
        'Programmet er konstrueret til dette øvelsessæt.'),
      situation='Ni år er slut. Nogle glæder sig til at komme videre. Andre '
        'havde ikke regnet med, at det ville føles så mærkeligt. I salen '
        'sidder din årgang, jeres lærere og en masse forældre, der ikke '
        'kender jeres historier.',
      rolle='Du er blevet spurgt, om du vil holde talen på årgangens vegne.',
      opgavetitel='Skriv din tale til afslutningen',
      forberedelse='Som forberedelse skal du tænke over, hvad der er værd '
        'at huske fra jeres tid sammen — også det, der ikke gik godt.',
      indled='I din tale skal du:',
      krav=[('fortælle', 'om mindst én konkret oplevelse, som årgangen deler'),
            ('beskrive', 'hvad I har lært, som ikke står i nogen bog'),
            ('tale til', 'både de unge og de voksne, der sidder i salen'),
            ('afslutte', 'med noget, publikum kan tage med sig hjem.')]),

 dict(titel='Kan man tro på det, man ser?',
      genre='Guide til skolens 6.- og 7.-klasser',
      kilder=[('https://www.dr.dk/nyheder/indland/hvert-tredje-barn-taenker-aldrig-over-foto-og-videoer-kan-vaere-manipulerede',
               'Hvert tredje barn tænker aldrig over, at foto og videoer kan '
               'være manipulerede',
               'En undersøgelse blandt 9-14-årige, altså præcis din '
               'målgruppe.'),
              ('https://www.dr.dk/nyheder/udland/ai-billeder-af-maduro-gaar-viralt-man-kan-efterhaanden-ikke-fortaenke-nogen-i-tro-det-er-aegte',
               'AI-billeder går viralt: man kan efterhånden ikke fortænke '
               'nogen i at tro, det er ægte',
               'Om hvor svært det er blevet at afgøre, hvad der er ægte.')],
      forlaeg=opslag('Fra skolens intranet',
        'Vi mangler materiale til 6.- og 7.-klasserne om billeder og videoer '
        'på nettet. Vi vil hellere have en guide skrevet af nogen, der selv '
        'er på de samme platforme, end en pjece udefra. Den skal kunne '
        'læses på fem minutter.',
        'Opslaget er konstrueret til dette øvelsessæt.'),
      situation='En video af en hval, der sluger en båd. Et billede af en '
        'kendt person i en situation, der aldrig fandt sted. Det tager i dag '
        'under en time at lave noget, der ligner virkeligheden til '
        'forveksling — og det bliver delt videre, længe før nogen tjekker '
        'efter.',
      rolle='Du skriver en guide, som skolens mindste klasser kan bruge.',
      opgavetitel='Skriv en guide til de mindste klasser',
      forberedelse='Som forberedelse skal du læse kilderne ovenfor og finde '
        'konkrete eksempler, du selv har set.',
      indled='I din guide skal du:',
      krav=[('forklare', 'hvad et AI-genereret billede eller en deepfake er, '
             'i et sprog en 12-årig forstår'),
            ('give', 'konkrete råd til, hvad man kigger efter, før man tror '
             'på noget'),
            ('bruge', 'overskrifter, punktopstilling eller andre virkemidler, '
             'så guiden er hurtig at læse'),
            ('slutte af', 'med, hvad man gør, hvis man er i tvivl.')]),

 dict(titel='Frivillig til festivalen', genre='Ansøgning', kilder=[],
      forlaeg=opslag('Vi søger unge frivillige',
        'Byens musikfestival mangler 40 frivillige mellem 15 og 20 år til '
        'boder, scener, affald og info. Du får mad, T-shirt og adgang til '
        'hele festivalen. Skriv til os, hvem du er, og hvad du gerne vil '
        'lave. Vi svarer alle.',
        'Opslaget er konstrueret til dette øvelsessæt.'),
      situation='Man skal ikke have prøvet det før for at søge. Men man skal '
        'kunne forklare, hvorfor lige præcis man selv er værd at sige ja til '
        '— og det er sværere, end det lyder, når man er 15 og aldrig har '
        'haft et job.',
      rolle='Du skriver en ansøgning til festivalens frivilligkoordinator.',
      opgavetitel='Skriv din ansøgning',
      forberedelse='Som forberedelse skal du beslutte, hvilken opgave på '
        'festivalen du søger.',
      indled='I din ansøgning skal du:',
      krav=[('præsentere', 'dig selv kort og skrive, hvad du søger'),
            ('beskrive', 'hvad du kan, og hvad du har erfaring med — også '
             'fra skole, fritid eller familie'),
            ('begrunde', 'hvorfor du gerne vil være med'),
            ('skrive', 'i en form og en tone, der passer til en, du ikke '
             'kender.')]),

 dict(titel='Det, jeg ikke fortalte', genre='Fortælling', kilder=[],
      forlaeg=opslag('Fra en opfordring til en antologi med tekster af unge',
        'Vi samler fortællinger om det, man ikke sagde højt. Det kan være '
        'stort eller lille: en løgn, en hemmelighed, noget man fortrød, '
        'eller noget man aldrig nåede at få sagt. Teksten må gerne være '
        'opdigtet.',
        'Opfordringen er konstrueret til dette øvelsessæt.'),
      situation='De fleste går rundt med noget, de ikke har fortalt nogen. '
        'Nogle gange fylder det ingenting. Andre gange fylder det alt.',
      rolle='Du skriver en fortælling til antologien. Den behøver ikke '
        'handle om dig selv.',
      opgavetitel='Skriv en fortælling',
      forberedelse='Som forberedelse skal du beslutte, hvem der fortæller '
        'historien, og hvornår læseren skal forstå, hvad der blev holdt '
        'tilbage.',
      indled='I din fortælling skal du:',
      krav=[('opbygge', 'en handling med et vendepunkt'),
            ('skildre', 'mindst én person, så læseren kan se og forstå ham '
             'eller hende'),
            ('bruge', 'miljø, replikker eller tanker til at skabe stemning'),
            ('give', 'fortællingen en titel, der passer til teksten.')]),
    ])

SAET['saet-3'] = dict(
    maerke='Sæt 3',
    kort='Et essay om det, man drømmer om, et debatindlæg om presset på '
         'skærmen, et oplæg om arbejde og maskiner, og en fortælling om året '
         'efter.',
    genrer=['essay', 'debatindlæg', 'mundtligt oplæg', 'fortælling'],
    opgaver=[
 dict(titel='Det, jeg skal være', genre='Essay',
      kilder=[], essay=True,
      forlaeg=citater(
        'Fire unge svarer på, hvad de skal efter 9. klasse:',
        [('Jeg siger gymnasiet, fordi så spørger folk ikke mere.',
          'Noa, 15 år'),
         ('Jeg vil gerne være noget med dyr. Det er ikke en uddannelse, det '
          'ved jeg godt.', 'Vera, 15 år'),
         ('Min mor siger, jeg skal tage det, der giver arbejde. Hun ved ikke, '
          'hvad der giver arbejde om ti år.', 'Mikkel, 16 år'),
         ('Jeg har skiftet mening fire gange i år. Det er vist meningen, at '
          'man ikke må det.', 'Alma, 15 år')],
        'Udsagnene er konstrueret til dette øvelsessæt.'),
      situation='I 9. klasse skal man vælge, før man ved nok. Spørgsmålet '
        'kommer fra alle sider — til middagen, til samtalen, fra folk man '
        'næsten ikke kender — og det forventes, at man har et svar.',
      rolle='Du skriver et essay om at skulle vælge en fremtid. Et essay må '
        'gerne være i tvivl: det skal ikke ende med et svar, men et sted, '
        'læseren kan tænke videre fra.',
      opgavetitel='Skriv et essay',
      forberedelse='Som forberedelse skal du læse vejledningen under '
        'menupunktet Essay og finde én konkret situation, du selv har '
        'stået i.',
      indled='I dit essay skal du:',
      krav=[('begynde', 'i noget helt konkret — en samtale, et svar du gav, '
             'et sted du stod'),
            ('bevæge dig', 'frem og tilbage mellem det konkrete og de store '
             'spørgsmål, det rejser'),
            ('undersøge', 'emnet fra flere vinkler i stedet for at '
             'konkludere med det samme'),
            ('slutte', 'et sted, der ikke lukker tanken.')]),

 dict(titel='Det perfekte liv på skærmen',
      genre='Debatindlæg til et medie for unge', kilder=[],
      forlaeg=opslag('Fra redaktionen',
        'Vi laver et tema om forventninger. Vi vil gerne have indlæg af '
        'unge, der selv er på de platforme, vi skriver om — ikke af voksne, '
        'der har læst en rapport. Tag stilling, og vær konkret.',
        'Opslaget er konstrueret til dette øvelsessæt.'),
      situation='På en skærm ser andres liv ud til at være redigeret '
        'færdigt. Man ved godt, at det er et udvalg. Man måler sig efter det '
        'alligevel. Nogle mener, at det er de unge selv, der skal lære at '
        'skrue ned. Andre mener, at det er platformene, der er indrettet '
        'sådan med vilje.',
      rolle='Du skriver et debatindlæg om presset for at være en bestemt '
        'slags person online.',
      opgavetitel='Skriv et debatindlæg',
      forberedelse='Som forberedelse skal du søge viden om unge og sociale '
        'medier og finde mindst ét tal, du kan bruge.',
      indled='I din tekst skal du:',
      krav=[('fortælle', 'om en konkret situation, du selv har set eller '
             'været i'),
            ('præsentere og kommentere', 'de vigtigste argumenter for, hvem '
             'ansvaret ligger hos'),
            ('argumentere', 'for dit eget synspunkt og tage det bedste '
             'modargument alvorligt'),
            ('foreslå', 'noget, der faktisk kan lade sig gøre.')]),

 dict(titel='Når maskinen kan det', genre='Mundtligt oplæg for 8. klasse',
      kilder=[],
      forlaeg=remse(
        'Fra en klasses liste over ting, de har brugt en AI til på en uge:',
        ['rette stavefejl', 'forklare en matematikopgave',
         'skrive en ansøgning om', 'finde på en overskrift',
         'oversætte til tysk', 'lave et billede til et oplæg'],
        'Listen er konstrueret til dette øvelsessæt.'),
      situation='Noget af det, voksne bliver betalt for i dag, kan en '
        'maskine gøre på et øjeblik. Noget andet kan den slet ikke. '
        'Grænsen flytter sig hurtigere, end nogen kan nå at planlægge '
        'efter — også dem, der skal rådgive jer om uddannelse.',
      rolle='8. klasse skal snart vælge valgfag og begynde at tænke på '
        'uddannelse. Du er blevet bedt om at holde et oplæg for dem om '
        'arbejde og maskiner.',
      opgavetitel='Skriv teksten til dit mundtlige oplæg',
      forberedelse='Som forberedelse skal du søge viden om, hvilke '
        'arbejdsopgaver der ændrer sig, og vælge to-tre eksempler, '
        'målgruppen kender.',
      indled='I dit oplæg skal du:',
      krav=[('forklare', 'hvad en AI er god til, og hvad den ikke er god til'),
            ('fortælle', 'om noget, du selv har brugt en maskine til — og '
             'hvad du lærte eller ikke lærte af det'),
            ('reflektere', 'over, hvad mennesker skal kunne, når maskinerne '
             'kan resten'),
            ('afslutte', 'med et råd, en 14-årig kan bruge, når der skal '
             'vælges valgfag.')]),

 dict(titel='Året efter', genre='Fortælling', kilder=[],
      forlaeg=opslag('Fra en skriveopfordring',
        'Skriv en fortælling, der foregår præcis ét år efter sidste '
        'skoledag. Vi er ikke ude efter en beskrivelse af fremtiden — vi er '
        'ude efter et menneske, der står et sted og mærker noget. Teksten '
        'må gerne være opdigtet.',
        'Opfordringen er konstrueret til dette øvelsessæt.'),
      situation='Et år er ikke lang tid. Alligevel er der sket noget: nogen '
        'er flyttet, nogen er holdt op, nogen er begyndt på noget, de ikke '
        'havde regnet med. Og nogen står samme sted som før.',
      rolle='Du skriver en fortælling, der foregår ét år efter sidste '
        'skoledag.',
      opgavetitel='Skriv en fortælling',
      forberedelse='Som forberedelse skal du beslutte, hvem der fortæller, '
        'og hvad den person ikke selv kan se.',
      indled='I din fortælling skal du:',
      krav=[('opbygge', 'en handling med et vendepunkt'),
            ('skildre', 'mindst én person, så læseren kan se og forstå ham '
             'eller hende'),
            ('bruge', 'miljø, replikker eller tanker til at skabe stemning'),
            ('give', 'fortællingen en titel, der passer til teksten.')]),
    ])

# ---------------------------------------------------- fælles på hvert sæt
FOER = [
 'Du har adgang til internettet, mens du skriver, men du må ikke '
 'kommunikere med andre eller dele dine dokumenter undervejs.',
 'Bruger du informationer, citater eller billeder fra nettet, skal kilderne '
 'stå til sidst i din besvarelse. Kilder, der allerede står i opgaven, '
 'behøver du ikke skrive op.',
]
HUSK = [
 'Skriv opgavens nummer og titel øverst i din besvarelse.',
 'Du får én karakter ud fra en samlet vurdering af de tre dimensioner: '
 'funktion, indhold og form.',
]

KRITERIER = [
 ('Funktion', [('Skrivesituation', 'I hvilken grad fungerer din tekst i den '
                'situation, opgaven beskriver?'),
               ('Opgavens krav', 'I hvilken grad opfylder du kravene til '
                'afsender, modtager og fremstillingsformer?')]),
 ('Indhold', [('Mening', 'I hvilken grad udtrykker din tekst et '
               'meningsfuldt indhold?'),
              ('Ressourcer', 'I hvilken grad bruger du forlægget, din egen '
               'viden og internettet i din tekst?')]),
 ('Form', [('Tekstsammenhæng', 'I hvilken grad hænger teksten sammen '
            'sprogligt, og er der velvalgte afsnit?'),
           ('Skrift og modaliteter', 'I hvilken grad understøtter '
            'tegnsætning, layout og ordvalg den situation, teksten skal '
            'bruges i?')]),
]

# Figuren til vurderingen. De tre dimensioner giver tilsammen én karakter -
# det staar i teksten, men det er lettere at se end at laese.
FIG_VURDERING = FG.afsaet(
    'Én karakter',
    ['Funktion — virker teksten i situationen?',
     'Indhold — siger den noget?',
     'Form — hænger den sammen?'],
    overskrift='SAMLET VURDERING')

# --------------------------------------------------------------- essayet
KENDETEGN = [
 ('Fri genre', 'Du blander egne oplevelser, tanker, følelser og '
  'observationer med generelle betragtninger.'),
 ('Undersøgende tone', 'Du starter ofte et sted i det helt konkrete — en '
  'hændelse, en genstand eller en situation — og "zoomer ud" for at '
  'reflektere over det store spørgsmål.'),
 ('Skrivetænkning', 'Teksten skal virke som en igangværende tankeproces, '
  'hvor du betragter emnet fra flere forskellige vinkler.'),
 ('Levende sprog', 'Brug billedsprog — metaforer, sammenligninger — '
  'sansninger og et personligt, men stadig præcist sprog.'),
]

# Kurverne viser en bevaegelse, ikke data. Pointen er forholdet mellem de tre.
KURVER = [('Stil', [.15, .20, .14, .22, .18, .15]),
          ('Kronik', [.80, .84, .80, .88, .84, .88]),
          ('Essay', [.22, .74, .30, .86, .34, .80])]
INDDELING = [('Indledning', 1), ('Hoveddel', 3), ('Afslutning', 1)]

GENNEMLAESNING = [('Gentagelser', 'står det samme to gange?'),
                  ('Udsagnsord', 'kan det blive mere præcist?'),
                  ('Tillægsord', 'fylder det bare?'),
                  ('Stavning', 'og kommaer')]

TRIN = [
 ('Læs opgaveformuleringen grundigt',
  ['Hvad er kernen i emnet? Hvilke tekster eller billeder følger med som '
   'afsæt, og hvordan kan du bruge dem som springbrættet til dine egne '
   'tanker?'], None, None),
 ('Brainstorm og find dit personlige vink',
  ['Spørg dig selv: Hvad betyder det her emne for mig? Hvornår har jeg '
   'oplevet noget lignende?',
   '<b>Undgå at skrive en kedelig stil eller en belærende kronik.</b>'],
  None, None),
 ('Byg essayet op',
  ['<b>Indledning.</b> Fang læseren med en skarp observation, en lille '
   'historie eller en undren. Undgå "I dette essay vil jeg …".',
   '<b>Hoveddel.</b> Bevæg dig frem og tilbage mellem det konkrete — en '
   'episode fra dit liv eller en detalje — og det abstrakte: tanker, '
   'filosofi, samfundet. Lad tankerne udvikle sig undervejs.',
   '<b>Afslutning.</b> Konkludér ikke med et tungt og kedeligt punktum, men '
   'lad tanken hænge i luften eller perspektivér til noget større.'],
  FG.konkret_abstrakt(KURVER, INDDELING),
  'Det er bevægelsen, der gør et essay til et essay. Stilen bliver nede i '
  'det konkrete, og kronikken bliver oppe i det abstrakte — essayet går op '
  'og ned mellem dem hele vejen igennem. Læg mærke til, at det ender oppe: '
  'tanken skal hænge i luften, ikke lukkes.'),
 ('Gennemlæs og spil sproget op',
  ['Er der for mange gentagelser? Kan du gøre et udsagnsord eller et '
   'tillægsord mere præcist? Tjek for basale retstavnings- og kommafejl.'],
  FG.kredsloeb(GENNEMLAESNING, ('Læs højt', 'en gang til')),
  'De fire spørgsmål, du stiller til din egen tekst. Læs højt — det er der, '
  'gentagelserne høres.'),
]

# ------------------------------------------------------------------ css
BASIS = open('funktioner-og-ligninger.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.jump a.aktiv{color:var(--accent);background:var(--accent-soft);
border-color:var(--accent-soft);font-weight:700}
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;
padding:18px;margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;text-align:left;
max-width:68ch;margin-left:auto;margin-right:auto}
h2.sec{font-size:1.4rem;margin:34px 0 6px;scroll-margin-top:72px}
p.sec{color:var(--muted);max-width:74ch;margin:0 0 12px;font-size:.97rem}
.boks{background:var(--panel2);border:1px solid var(--line);
border-left:4px solid var(--accent);border-radius:12px;padding:16px 20px;
margin:16px 0}
.boks h3{font-size:1.05rem;margin:0 0 4px}
.boks p,.boks li{color:var(--muted);font-size:.95rem;max-width:74ch}
.boks ul{margin:6px 0 0;padding-left:20px}
.boks li{margin:4px 0}
table.krit{width:100%;border-collapse:collapse;margin:10px 0;font-size:.92rem}
table.krit th,table.krit td{border:1px solid var(--line);padding:9px 11px;
text-align:left;vertical-align:top}
table.krit thead th{background:var(--panel2);font-size:.8rem;
text-transform:uppercase;letter-spacing:.4px;color:var(--muted)}
table.krit td.dim{font-weight:800;background:var(--panel2);width:14%}
table.krit td.omr{width:24%;font-weight:600}
.vaelg{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
gap:10px;margin:10px 0 0}
.vaelg a{display:block;text-decoration:none;background:var(--panel);
border:1px solid var(--line);border-radius:12px;padding:12px 14px;
color:var(--ink);font-weight:700;font-size:.97rem}
.vaelg a:hover{border-color:var(--accent)}
.vaelg span{display:block;color:var(--muted);font-weight:400;font-size:.84rem;
margin-top:3px}
.opg{background:var(--panel);border:1px solid var(--line);border-radius:16px;
padding:22px 26px;margin:18px 0;box-shadow:var(--shadow);
scroll-margin-top:72px}
.opg > h3{font-size:1.35rem;margin:0;display:flex;align-items:baseline;gap:12px}
.opg > h3 .nr{flex:0 0 auto;width:30px;height:30px;border-radius:9px;
background:var(--accent);color:#fff;display:grid;place-items:center;
font-size:.95rem;font-weight:800;align-self:center}
.opg .genre{color:var(--muted);font-weight:600;font-size:.95rem;
margin:2px 0 14px 42px}
.opg h4{font-size:.82rem;text-transform:uppercase;letter-spacing:.5px;
color:var(--muted);margin:18px 0 6px}
.opg p{color:var(--muted);font-size:.97rem;max-width:74ch;margin:8px 0}
.opg p b{color:var(--ink)}
.kilder{list-style:none;padding:0;margin:0}
.kilder li{margin:8px 0;padding-left:16px;border-left:3px solid var(--line)}
.kilder a{font-weight:700;color:var(--accent);text-decoration:none}
.kilder a:hover{text-decoration:underline}
.kilder span{display:block;color:var(--muted);font-size:.9rem;margin-top:2px}
.kildenavn{color:var(--muted);font-size:.84rem;margin-top:8px}
.forlaeg{background:var(--panel2);border:1px solid var(--line);
border-radius:12px;padding:16px 20px;margin:6px 0 0}
.forlaeg-ind{margin:0 0 10px!important;color:var(--ink)!important;
font-weight:600}
.cit{display:grid;gap:10px}
.forlaeg blockquote{margin:0;padding:10px 14px;background:#fff;
border:1px solid var(--line);border-radius:10px;font-size:.96rem;
color:var(--ink)}
.forlaeg cite{display:block;font-style:normal;color:var(--muted);
font-size:.85rem;margin-top:6px}
.remse{font-family:"Consolas",monospace;font-size:.92rem;color:var(--ink)!important;
background:#fff;border:1px solid var(--line);border-radius:10px;
padding:12px 14px;margin:0!important;line-height:1.9}
.opslag{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:14px 16px}
.opslag h5{margin:0 0 6px;font-size:1.02rem}
.opslag p{margin:0!important;font-size:.96rem}
ul.prog{list-style:none;margin:0;padding:0;background:#fff;
border:1px solid var(--line);border-radius:10px;padding:12px 16px}
ul.prog li{display:flex;gap:14px;padding:4px 0;font-size:.95rem;
color:var(--muted)}
ul.prog .tid{font-family:"Consolas",monospace;color:var(--accent);
flex:0 0 52px}
ul.prog b{color:var(--ink)}
.konstrueret{font-size:.84rem!important;font-style:italic;margin:10px 0 0!important}
ol.krav{margin:4px 0 0;padding-left:20px}
ol.krav li{color:var(--muted);font-size:.97rem;margin:7px 0;max-width:72ch}
ol.krav b{color:var(--accent);font-weight:800}
.afsnit{background:var(--panel);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:14px 0;box-shadow:var(--shadow)}
.afsnit h2{font-size:1.2rem;margin:0 0 10px;display:flex;align-items:center;
gap:12px;border:0;padding:0}
.afsnit .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.afsnit p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:74ch}
.afsnit p b{color:var(--ink)}
table.liste{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.liste th,table.liste td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.liste th{background:var(--panel2);width:26%}
.kortnet{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));
gap:18px;margin:14px 0 0}
.kort{display:block;text-decoration:none;color:inherit;background:var(--panel);
border:1px solid var(--line);border-radius:16px;padding:22px 24px;
box-shadow:var(--shadow);transition:.15s}
.kort:hover{border-color:var(--accent);transform:translateY(-2px)}
.kort .uge{font-family:"Consolas",monospace;font-size:.74rem;
letter-spacing:.6px;text-transform:uppercase;color:var(--accent);
font-weight:700}
.kort h2{font-size:1.3rem;margin:6px 0 8px;border:0;padding:0}
.kort p{color:var(--muted);margin:0 0 14px;font-size:.96rem}
.kort ul{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;
gap:6px;font-size:.77rem;font-family:"Consolas",monospace;color:var(--accent)}
.kort li{background:var(--accent-soft);padding:4px 9px;border-radius:20px}
.printbtn{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:10px 18px;font-weight:700;font-size:.95rem;cursor:pointer;
color:var(--ink);font-family:inherit;margin:6px 8px 0 0}
.printbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{header.top,.printbtn,.vaelg{display:none!important}
.opg,.afsnit,.figur,.boks{box-shadow:none;break-inside:avoid;
page-break-inside:avoid}
body{font-size:10.5pt}main{padding:0}@page{size:A4;margin:14mm}}
'''


def side(noegle, titel, krop):
    """Skriver én selvbaerende side. Menuen peger paa de omskrevne adresser
    (/dansk/saet-1), for det er dem, browseren staar paa."""
    menu = ''.join(
        f'<a class="{"aktiv" if n == noegle else ""}" href="/dansk/{n}">'
        f'{m}</a>' for n, m in SIDER.items())
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            # Siden er ulistet. noindex holder den ude af soegemaskinerne;
            # den beskytter ikke mod nogen, der har adressen.
            '<meta name="robots" content="noindex, nofollow">'
            f'<title>{html.escape(titel)}</title><style>' + CSS
            + '</style></head><body><header class="top"><div class="top-inner">'
            '<a class="brand" href="/dansk" style="text-decoration:none;'
            'color:inherit">Dansk · <span>9. klasse</span></a>'
            f'<nav class="jump">{menu}</nav></div></header><main>' + krop
            + '</main><footer>Øvelsessæt til undervisningsbrug · dansk, '
              'skriftlig fremstilling · Mibelibsen.</footer></body></html>')


def kriterier_html():
    r = ''
    for dim, omr in KRITERIER:
        for i, (navn, spm) in enumerate(omr):
            r += '<tr>'
            if i == 0:
                r += f'<td class="dim" rowspan="{len(omr)}">{dim}</td>'
            r += (f'<td class="omr">{html.escape(navn)}</td>'
                  f'<td>{html.escape(spm)}</td></tr>')
    return ('<table class="krit"><thead><tr><th>Dimension</th><th>Område</th>'
            f'<th>Spørgsmål</th></tr></thead><tbody>{r}</tbody></table>')


def opgave_html(nr, o):
    s = (f'<section class="opg" id="opgave-{nr}"><h3>'
         f'<span class="nr">{nr}</span>{html.escape(o["titel"])}</h3>'
         f'<p class="genre">{html.escape(o["genre"])}</p>')
    if o['kilder']:
        s += '<h4>Se og læs, inden du skriver</h4><ul class="kilder">'
        for url, overskrift, beskriv in o['kilder']:
            s += (f'<li><a href="{url}" target="_blank" rel="noopener">'
                  f'{html.escape(overskrift)}</a>'
                  f'<span>{html.escape(beskriv)}</span></li>')
        s += '</ul><p class="kildenavn">Kilde: dr.dk</p>'
    s += f'<h4>Forlæg</h4><div class="forlaeg">{o["forlaeg"]}</div>'
    s += (f'<p>{html.escape(o["situation"])}</p>'
          f'<p><b>{html.escape(o["rolle"])}</b></p>'
          f'<h4>Opgave</h4><p><b>{html.escape(o["opgavetitel"])}</b></p>'
          f'<p>{html.escape(o["forberedelse"])}</p>'
          f'<p>{html.escape(o["indled"])}</p><ol class="krav">')
    for udsagnsord, rest in o['krav']:
        s += f'<li><b>{html.escape(udsagnsord)}</b> {html.escape(rest)}</li>'
    return s + '</ol></section>'


def byg_saet(noegle):
    d = SAET[noegle]
    foer = ''.join(f'<li>{html.escape(t)}</li>' for t in FOER)
    husk = ''.join(f'<li>{html.escape(t)}</li>' for t in HUSK)
    vaelg = ''.join(
        f'<a href="#opgave-{i}">{i}. {html.escape(o["titel"])}'
        f'<span>{html.escape(o["genre"])}</span></a>'
        for i, o in enumerate(d['opgaver'], 1))
    krop = (f'<section class="hero"><span class="pill">Skriftlig '
            f'fremstilling · {d["maerke"].lower()}</span>'
            f'<h1>Øvelsessæt i skriftlig fremstilling</h1>'
            f'<p>Fire opgaver i samme form som til prøven. Du vælger én af '
            f'dem og skriver din tekst i et tekstbehandlingsprogram. Du har '
            f'adgang til internettet undervejs.</p>'
            f'<button class="printbtn" onclick="window.print()">'
            f'Udskriv sættet</button></section>'
            f'<div class="boks"><h3>Før du skriver</h3>'
            f'<p>Læs det her, inden du vælger opgave.</p><ul>{foer}</ul>'
            f'<h3 style="margin-top:14px">Husk</h3><ul>{husk}</ul></div>'
            f'<h2 class="sec">Vurderingskriterier</h2>'
            f'<div class="figur">{FIG_VURDERING}'
            f'<div class="figtekst">Du får <b>én</b> karakter. Den er en '
            f'samlet vurdering af alle tre dimensioner — en tekst, der '
            f'hænger fint sammen, men ikke virker i situationen, er ikke '
            f'halvt så god, den er noget andet.</div></div>'
            + kriterier_html()
            + f'<h2 class="sec">Du skal vælge én af disse fire opgaver</h2>'
            f'<div class="vaelg">{vaelg}</div>'
            + ''.join(opgave_html(i, o)
                      for i, o in enumerate(d['opgaver'], 1))
            + '<button class="printbtn" onclick="window.print()">'
              'Udskriv sættet</button>')
    return side(noegle, f'Skriftlig fremstilling · {d["maerke"]} · 9. klasse',
                krop)


def byg_essay():
    kendetegn = ''.join(f'<tr><th>{html.escape(a)}</th><td>{b}</td></tr>'
                        for a, b in KENDETEGN)
    trin = ''
    for i, (o, stykker, figur, figtekst) in enumerate(TRIN, 1):
        trin += (f'<section class="afsnit"><h2><span class="num">{i}</span>'
                 f'{html.escape(o)}</h2>'
                 + ''.join(f'<p>{t}</p>' for t in stykker))
        if figur:
            trin += (f'<div class="figur">{figur}'
                     f'<div class="figtekst">{figtekst}</div></div>')
        trin += '</section>'
    krop = ('<section class="hero"><span class="pill">Skriftlig '
            'fremstilling · genre</span><h1>Essay</h1>'
            '<p>Essayet er den frieste af genrerne, og det er derfor, den er '
            'svær. Her er, hvad den kræver, og hvordan du kommer igennem '
            'skriveprocessen. Opgave 1 i <a href="/dansk/saet-3">Sæt 3</a> '
            'er et essay.</p>'
            '<button class="printbtn" onclick="window.print()">'
            'Print siden</button></section>'
            '<h2 class="sec">Hvad kendetegner et essay?</h2>'
            f'<table class="liste"><tbody>{kendetegn}</tbody></table>'
            '<h2 class="sec">Trin for trin gennem skriveprocessen</h2>'
            f'{trin}'
            '<button class="printbtn" onclick="window.print()">'
            'Print siden</button>')
    return side('essay', 'Essay · skriftlig fremstilling · 9. klasse', krop)


def byg_forside():
    kort = ''
    for noegle in ('saet-1', 'saet-2', 'saet-3'):
        d = SAET[noegle]
        genrer = ''.join(f'<li>{html.escape(g)}</li>' for g in d['genrer'])
        kort += (f'<a class="kort" href="/dansk/{noegle}">'
                 f'<span class="uge">{d["maerke"]} · fire opgaver</span>'
                 f'<h2>Skriftlig fremstilling</h2>'
                 f'<p>{html.escape(d["kort"])}</p><ul>{genrer}</ul></a>')
    krop = ('<section class="hero"><span class="pill">Skriftlig '
            'fremstilling</span><h1>Dansk i 9. klasse</h1>'
            '<p>Øvelsessæt i skriftlig fremstilling, bygget op som til '
            'prøven. Hvert sæt har fire opgaver, du vælger mellem, og en '
            'side med vurderingskriterierne. Sættene kan skrives på tid '
            'eller udskrives.</p></section>'
            f'<div class="kortnet">{kort}</div>'
            '<h2 class="sec">Essay</h2>'
            '<p class="sec">Opgave 1 i Sæt 3 er et essay. Genren er fri, og '
            'det er derfor, den er svær — vejledningen står for sig selv.</p>'
            '<div class="vaelg"><a href="/dansk/essay">Essay · '
            'sådan skriver du et<span>Kendetegn, opbygning og de fire trin '
            'i skriveprocessen</span></a></div>'
            '<h2 class="sec">Sådan bliver din tekst vurderet</h2>'
            '<p class="sec">Det samme gælder i alle tre sæt, og det står '
            'også øverst på hvert sæt.</p>'
            f'<div class="figur">{FIG_VURDERING}<div class="figtekst">'
            'Du får <b>én</b> karakter. Den er en samlet vurdering af alle '
            'tre dimensioner — en tekst, der hænger fint sammen, men ikke '
            'virker i situationen, er ikke halvt så god, den er noget '
            'andet.</div></div>'
            + kriterier_html())
    return side(None, 'Dansk · skriftlig fremstilling · 9. klasse', krop)


if __name__ == '__main__':
    assert set(SAET) | {'essay'} == set(SIDER), 'siderne og menuen passer ikke'
    for noegle in SAET:
        assert len(SAET[noegle]['opgaver']) == 4, f'{noegle} har ikke fire opgaver'
        assert len(SAET[noegle]['genrer']) == 4, f'{noegle}: fire genrer'
        for o in SAET[noegle]['opgaver']:
            assert len(o['krav']) == 4, f'{o["titel"]} har ikke fire krav'
    ialt = 0
    for navn, dok in [(fil(None), byg_forside()), (fil('essay'), byg_essay())] \
            + [(fil(n), byg_saet(n)) for n in SAET]:
        open(navn, 'w', encoding='utf-8').write(dok)
        ialt += dok.count('<svg')
        print(f'skrevet:  {navn}')
    print(f'{len(SAET)} sæt · {sum(len(s["opgaver"]) for s in SAET.values())} '
          f'opgaver · {ialt} figurer')
