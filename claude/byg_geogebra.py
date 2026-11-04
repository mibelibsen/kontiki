# -*- coding: utf-8 -*-
"""Bygger Intro til GeoGebra - vejledningen til opgave C og D.

Siden ligger i roden og udgives, men **ingen side linker til den**. Den kan
kun naas, hvis man kender adressen. Ulistet er ikke privat: har man
adressen, kan man laese den.

**Der staar ingen facit paa siden.** Alle eksempler bruger tal, der ikke
findes i opgave C eller D, saa ungerne kan foelge fremgangsmaaden uden at
faa svaret foraeret.

Kommandonavnene er proevet af i GeoGebra Classic paa dansk, ikke husket:
Linje, Haeldning, Rod og Skaering er dem, programmet selv skriver i
algebravinduet. "Nulpunkt" findes ikke - den hedder Rod.

**Skaermbillederne er taget i den rigtige app**, ikke tegnet: et script
aabner geogebra.org/classic i Chromium paa dansk, skriver kommandoerne og
fotograferer vinduet. Filerne ligger i billeder/geogebra/ og bygges af
claude/hent_geogebra_billeder.mjs. Bliver GeoGebras udseende aendret,
koeres det script igen - billederne maa ikke tegnes i haanden, for saa
holder de op med at ligne det, ungen ser.

    python3 claude/byg_geogebra.py
"""
import html
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figurer as FG

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = 'geogebra-lineaere-funktioner.html'
GEOGEBRA = 'https://www.geogebra.org/classic?lang=da'
BILLEDER = 'billeder/geogebra'


# --------------------------------------------------------------------- ikoner
def _ikon_graf():
    """GeoGebras Graf-ikon: en bølget kurve. Punkterne regnes."""
    pkt = [(3 + 16 * i / 48, 11 - 5.5 * math.sin(2 * math.pi * i / 48))
           for i in range(49)]
    d = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in pkt)
    return ('<svg class="ikon" viewBox="0 0 22 22" aria-hidden="true">'
            f'<path d="{d}" fill="none" stroke="#6557d6" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _ikon_menu():
    """De tre streger øverst til højre."""
    linjer = ''.join(f'<line x1="4" y1="{y}" x2="18" y2="{y}"/>'
                     for y in (6.5, 11, 15.5))
    return ('<svg class="ikon" viewBox="0 0 22 22" aria-hidden="true">'
            f'<g stroke="#1a2233" stroke-width="1.8" stroke-linecap="round">'
            f'{linjer}</g></svg>')


IKON_GRAF, IKON_MENU = _ikon_graf(), _ikon_menu()


def _ikon_advarsel():
    """En trekant med et udråbstegn. Punkterne regnes, så den er ligesidet."""
    h = 17 * math.sqrt(3) / 2
    pkt = f'11,{11 - h/2:.2f} {11 - 8.5:.2f},{11 + h/2:.2f} {11 + 8.5:.2f},{11 + h/2:.2f}'
    return ('<svg class="ikon" viewBox="0 0 22 22" aria-hidden="true">'
            f'<polygon points="{pkt}" fill="#ffe9d6" stroke="#d98324" '
            'stroke-width="1.6" stroke-linejoin="round"/>'
            '<line x1="11" y1="8.5" x2="11" y2="13.5" stroke="#d98324" '
            'stroke-width="1.8" stroke-linecap="round"/>'
            '<circle cx="11" cy="16.2" r="1.1" fill="#d98324"/></svg>')


IKON_ADVARSEL = _ikon_advarsel()


# ------------------------------------------------- figuren til ligningsflytten
def fig_flyt(venstre='-2x + y = 1', hojre='y = 2x + 1',
             fra=(0, 3), til=(4, 6)):
    """Viser, hvordan -2x + y = 1 bliver til y = 2x + 1.

    Teksten saettes med fast bredde, saa hvert tegns plads kan REGNES: i en
    monospace-skrift er et tegn 0,6 gange skriftstoerrelsen bredt. Derfor
    kan rammen om leddet og pilen imellem dem laegges praecist i stedet for
    at blive skubbet paa plads paa oejemaal. Teksterne til hoejre er
    hoejrestillede, og pilens forklaring ligger UNDER ligningerne - foerst
    laa den oven i dem."""
    fs, x0, W = 21, 26, 520
    w = fs * 0.6
    y1, y2 = 42, 118
    a1, a2 = x0 + fra[0] * w, x0 + fra[1] * w
    b1, b2 = x0 + til[0] * w, x0 + til[1] * w
    mx1, mx2 = (a1 + a2) / 2, (b1 + b2) / 2
    bue = (f'M{mx1:.1f},{y1 + 9} Q{(mx1 + mx2) / 2 - 14:.1f},'
           f'{(y1 + y2) / 2 + 16:.0f} {mx2:.1f},{y2 - 18}')
    # Teksten til hoejre maa ikke naa ind over ligningen.
    assert x0 + max(len(venstre), len(hojre)) * w < W - 150

    def ramme(x, y):
        return (f'<rect x="{x - 3:.1f}" y="{y - fs + 3}" '
                f'width="{(a2 - a1) if x == a1 else (b2 - b1):.1f}" '
                f'height="{fs + 6}" rx="4" fill="#ffe9d6" stroke="#d98324" '
                f'stroke-width="1"/>')

    def tekst(x, y, s, **kw):
        ekstra = ''.join(f' {k.replace("_", "-")}="{v}"' for k, v in kw.items())
        return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" '
                f'font-family="Consolas, monospace" fill="#1a2233" '
                f'xml:space="preserve"{ekstra}>{html.escape(s)}</text>')

    return (
        f'<svg viewBox="0 0 {W} 172" class="flyt" '
        'xmlns="http://www.w3.org/2000/svg" role="img" '
        'aria-label="Sådan flyttes leddet over på den anden side">'
        f'<rect x="{a1 - 3:.1f}" y="{y1 - fs + 3}" width="{a2 - a1 + 6:.1f}" '
        f'height="{fs + 6}" rx="4" fill="#ffe9d6" stroke="#d98324" '
        f'stroke-width="1"/>'
        f'<rect x="{b1 - 3:.1f}" y="{y2 - fs + 3}" width="{b2 - b1 + 6:.1f}" '
        f'height="{fs + 6}" rx="4" fill="#ffe9d6" stroke="#d98324" '
        f'stroke-width="1"/>'
        + tekst(x0, y1, venstre) + tekst(x0, y2, hojre)
        + f'<path d="{bue}" fill="none" stroke="#d98324" stroke-width="2" '
          f'marker-end="url(#spids)"/>'
        '<defs><marker id="spids" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#d98324"/></marker></defs>'
        f'<text x="{x0}" y="158" font-size="13" fill="#d98324" '
        f'font-weight="700">Leddet flytter over — og skifter fortegn</text>'
        f'<text x="{W - 10}" y="{y1}" font-size="12.5" fill="#586074" '
        f'text-anchor="end">sådan skriver GeoGebra den</text>'
        f'<text x="{W - 10}" y="{y2}" font-size="12.5" fill="#586074" '
        f'text-anchor="end">sådan skal du bruge den</text>'
        '</svg>')


# ---------------------------------------------------------------- eksempeltal
# De maa IKKE vaere opgavernes egne. y = 2x + 1 gaar gennem (1,3) og (4,9);
# y = x + 4 skaerer den i (3,7). Alle tal er pæne, og ingen af dem staar i
# opgave C eller D.
EKS_A, EKS_B = 2, 1
P1, P2 = (1, 3), (4, 9)
EKS2_A, EKS2_B = 1, 4
SKAER = (3, 7)
VAERDI_X = 7
VAERDI_Y = EKS_A * VAERDI_X + EKS_B
NULPUNKT = -EKS_B / EKS_A
assert EKS_A * P1[0] + EKS_B == P1[1] and EKS_A * P2[0] + EKS_B == P2[1]
assert EKS_A * SKAER[0] + EKS_B == SKAER[1] == EKS2_A * SKAER[0] + EKS2_B
assert VAERDI_Y == 15, 'skærmbilledet 11-vaerdi.png viser g(7) = 15'

FIG_LINJE = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f')],
    punkter=[(P1[0], P1[1], FG.ROD, 'A'), (P2[0], P2[1], FG.ROD, 'B')],
    xmin=-1, xmax=6, ymin=-1, ymax=11,
    trappe=(EKS_A, EKS_B, P1[0], P2[0] - P1[0]))

FIG_SKAER = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f'), (EKS2_A, EKS2_B, FG.GRO, 'g')],
    punkter=[(SKAER[0], SKAER[1], FG.ROD, 'S')],
    xmin=-1, xmax=6, ymin=-1, ymax=11)

# Fire billeder af den SAMME ting, fordi hældningen er det, flest falder
# over: ét trin, fem trin, et trin nedad, og den anden vej rundt — at
# tegne linjen ud fra a og b. Koordinaterne regnes af figurer.py.
FIG_TRIN1 = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f')],
    xmin=-1, xmax=6, ymin=-1, ymax=11, trappe=(EKS_A, EKS_B, 1))

FIG_TRIN5 = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f')],
    xmin=-1, xmax=6, ymin=-1, ymax=11, trappe=(EKS_A, EKS_B, 0, 5))

NED_A, NED_B = -2, 9
FIG_TRINNED = FG.koordinatsystem(
    linjer=[(NED_A, NED_B, FG.GRO, 'h')],
    xmin=-1, xmax=6, ymin=-1, ymax=11, trappe=(NED_A, NED_B, 1))

FIG_TEGN = FG.koordinatsystem(
    linjer=[(EKS_A, EKS_B, FG.BLA, 'f')],
    punkter=[(0, EKS_B, FG.ROD, 'b'), (1, EKS_A + EKS_B, FG.ROD, '')],
    xmin=-1, xmax=6, ymin=-1, ymax=11, trappe=(EKS_A, EKS_B, 0))

assert NED_A * 1 + NED_B == 7 and NED_A * 2 + NED_B == 5, 'trinnet nedad'
assert EKS_A * 5 == 10, 'fem til højre skal give ti op'



# (overskrift, [afsnit], [(skriv, sker)], figur, figurtekst, [(billede, tekst)])
TRIN = [
 ('Åbn GeoGebra, og vælg Graf',
  ['Gå ind på <b>geogebra.org/classic</b>. Du skal ikke logge ind, og du '
   'skal ikke hente noget.',
   f'<div class="ikonboks">{IKON_GRAF}<p>Første gang siden åbner, kommer '
   f'der en liste frem i højre side. <b>Vælg den øverste: Graf.</b> Det er '
   f'det eneste sted, ordet «Graf» står.</p></div>',
   f'<div class="ikonboks">{IKON_MENU}<p>Kommer listen ikke frem, er du '
   f'allerede i Graf — så gå bare videre. Du kan altid finde listen igen: '
   f'klik på de tre streger øverst til højre, og vælg '
   f'<b>Perspektiv</b>.</p></div>',
   'Alt, hvad du skriver i Input-feltet, afsluttes med <b>Enter</b>.'],
  [], None, None,
  [('1-vaelg-graf.png', 'Listen, der kommer frem. Vælg Graf — den øverste.'),
   ('2-vinduet.png',
    'Sådan ser vinduet ud bagefter. Til venstre er algebravinduet med '
    'feltet Input… — det er dér, du skriver. Til højre er grafikvinduet, '
    'hvor tingene bliver tegnet. Kan du se de to ting, er du det rigtige '
    'sted.')]),

 ('Sæt de to punkter ind',
  ['Har du to målinger — to kvitteringer, to aflæsninger — så er de to '
   'punkter. Skriv dem ét ad gangen, og tryk Enter efter hvert.',
   'Pas på kommaet: koordinater skrives <code class="inl">(1,3)</code>. '
   'Decimaltal skrives med <b>punktum</b> i GeoGebra, så 2,5 skrives '
   '<code class="inl">2.5</code>.'],
  [('A=(1,3)', 'Punktet A dukker op i grafikvinduet'),
   ('B=(4,9)', 'Punktet B kommer også')],
  None, None,
  [('3-punkter.png',
    'De to punkter står nu både i algebravinduet til venstre og i '
    'grafikvinduet til højre. Ser du dem ikke, så rul ud med musehjulet.')]),

 ('Tegn linjen gennem dem',
  ['Nu trækker du linjen gennem de to punkter. Den får automatisk navnet '
   '<code class="inl">f</code>.',
   '<b>Her kommer en overraskelse.</b> GeoGebra skriver ikke linjen som '
   '<code class="inl">y = ax + b</code>. Der står '
   '<code class="inl">-2x + y = 1</code>. Det er den <i>samme</i> linje, '
   'bare skrevet på en anden måde — og du skal selv skrive den om.'],
  [('Linje(A,B)', 'Linjen tegnes, og dens ligning står i algebravinduet')],
  None, None,
  [('4b-ligningen.png',
    'Sådan står der i algebravinduet. f: Linje(A, B), og nedenunder '
    'ligningen -2x + y = 1.')]),

 ('Skriv ligningen om, så den bliver til y = ax + b',
  [f'<div class="advarsel">{IKON_ADVARSEL}<p><b>Ret ikke i den linje, der '
   f'allerede står i GeoGebra.</b> Omskrivningen her laver du på papiret '
   f'eller i hovedet — ikke i programmet. Og alt, hvad du senere skriver i '
   f'GeoGebra, skriver du på en <b>ny linje</b> i feltet <i>Input…</i> '
   f'nederst i algebravinduet. Klikker du op i en linje, der står der i '
   f'forvejen, laver du den om i stedet for at lave en ny — og så flytter '
   f'linjen sig.</p></div>',
   'Du vil have <code class="inl">y</code> til at stå <b>alene</b> på '
   'venstre side. Lige nu står der <code class="inl">-2x</code> i vejen.',
   '<b>1.</b> Læg <code class="inl">2x</code> til på <b>begge</b> sider af '
   'lighedstegnet. Det må man altid, så længe man gør det samme på begge '
   'sider.',
   '<b>2.</b> På venstre side går <code class="inl">-2x + 2x</code> ud med '
   'hinanden. Tilbage står <code class="inl">y</code> helt alene.',
   '<b>3.</b> På højre side bliver <code class="inl">1</code> til '
   '<code class="inl">2x + 1</code>.',
   'Altså <code class="inl">y = 2x + 1</code>. '
   '<b>Huskereglen:</b> flytter du et led over på den anden side af '
   'lighedstegnet, skifter det fortegn. Minus bliver til plus, plus bliver '
   'til minus. Leddet forsvinder ikke — det flytter.',
   '<b>Tjek til sidst:</b> sæt et af dine punkter ind. Med A = (1, 3): '
   '2 · 1 + 1 = 3. Det passer, så omskrivningen er rigtig.'],
  [], 'FLYT',
  'Leddet -2x flytter over på den anden side og skifter fortegn. Alt '
  'andet står, hvor det stod.', []),

 ('Hældningen a — og hvordan du tegner den',
  ['Kommandoen hedder <b>Hældning</b>. Skriv '
   '<code class="inl">Hældning(f)</code> på en <b>ny linje</b>. GeoGebra '
   'svarer med et tal — og tegner samtidig en lille orange figur ude på '
   'linjen. <b>Figuren er det vigtigste, ikke tallet.</b>',
   'Den hedder et <b>trappetrin</b>, og den viser, hvad hældningen '
   '<i>er</i>: hvor meget linjen går op, hver gang du går <b>én til '
   'højre</b>. Ikke andet.',
   '<b>Sådan tegner du trappetrinnet selv, på papir:</b>',
   '<b>1.</b> Sæt blyanten på et sted, hvor linjen rammer et hjørne i '
   'ternene. Det er lettere at tælle fra.',
   '<b>2.</b> Gå <b>1 tern til højre</b>, og tegn den vandrette streg.',
   '<b>3.</b> Gå <b>lodret</b> op, til du rammer linjen igen. Tegn den '
   'lodrette streg.',
   '<b>4.</b> Tæl, hvor mange tern du gik op. Det tal er '
   '<code class="inl">a</code>.',
   f'<div class="figur">{FIG_TRIN1}<div class="figtekst">Her er der gået '
   f'1 til højre og {EKS_A} op, så a = {EKS_A}. Den stiplede vinkel er '
   f'præcis den, GeoGebra tegner for dig.</div></div>',
   '<b>Når 1 til højre ikke rammer et hjørne,</b> så gå længere. Gå '
   '<b>5 til højre</b>, tæl hvor mange du går op, og <b>divider med '
   '5</b> til sidst. Det giver det samme tal — og det er præcis den '
   'fremgangsmåde, opgaven beder om.',
   f'<div class="figur">{FIG_TRIN5}<div class="figtekst">5 til højre og '
   f'{EKS_A * 5} op. {EKS_A * 5} ÷ 5 = {EKS_A}. Samme hældning, bare '
   f'talt over et længere stykke — og nemmere at aflæse rigtigt.'
   f'</div></div>',
   '<b>Når linjen falder,</b> går du <b>ned</b> i stedet for op, og så '
   'er <code class="inl">a</code> <b>negativ</b>. Trappetrinnet vender '
   'nedad. Det sker i batteridelen af opgave C: batteriet bliver mindre, '
   'ikke større.',
   f'<div class="figur">{FIG_TRINNED}<div class="figtekst">1 til højre og '
   f'{abs(NED_A)} ned giver a = {NED_A}. Minusset er ikke en fejl — det '
   f'er hele oplysningen om, at linjen går nedad.</div></div>',
   '<b>Og den anden vej rundt: tegn linjen ud fra a og b.</b> Det er her, '
   'hældningen holder op med at være et tal, du slår op, og bliver noget, '
   'du kan bruge:',
   '<b>1.</b> Sæt et punkt på y-aksen i højden <code class="inl">b</code>.',
   '<b>2.</b> Gå 1 til højre og <code class="inl">a</code> op. Sæt et '
   'punkt mere.',
   '<b>3.</b> Træk linjen gennem de to punkter — og forlæng den til begge '
   'sider.',
   f'<div class="figur">{FIG_TEGN}<div class="figtekst">Fra b på y-aksen: '
   f'1 til højre, {EKS_A} op, og der er det næste punkt. '
   f'<b>Hældningen er en opskrift på at komme fra ét punkt på linjen til '
   f'det næste</b> — ikke bare et tal.</div></div>',
   '<b>Tjek dig selv:</b> skriv <code class="inl">Hældning(g)</code> på '
   'din egen funktion, når du har lavet den i næste trin. Får du det '
   'samme tal, er den rigtig.'],
  [('Hældning(f)', 'Tallet a kommer frem, og trappetrinnet tegnes på linjen')],
  None, None,
  [('5-haeldning.png',
    'I algebravinduet står a = Hældning(f) og nedenunder = 2. Ude på '
    'linjen er trappetrinnet tegnet med 1 til højre og 2 op.')]),

 ('Aflæs b, og skriv din egen forskrift',
  ['<code class="inl">b</code> er dér, hvor linjen skærer <b>y-aksen</b> — '
   'den lodrette. Kig i grafikvinduet: her krydser linjen i 1, så '
   'b = 1.',
   'Nu har du både <code class="inl">a</code> og <code class="inl">b</code>. '
   '<b>Skriv selv forskriften</b>, og giv den et nyt navn, fx '
   '<code class="inl">g</code>. Skriv <code class="inl">g(x)=</code> foran — '
   'så bliver det en <b>funktion</b>, og så virker de næste kommandoer.',
   '<b>Sådan tjekker du dig selv:</b> hvis din forskrift er rigtig, lægger '
   '<code class="inl">g</code> sig præcis oven på <code class="inl">f</code>, '
   'og du kan ikke se to linjer. Kan du se to, er der en fejl i a eller b.'],
  [('g(x)=2x+1', 'Din egen forskrift tegnes — den skal dække linjen f')],
  None, None,
  [('6-egen-forskrift.png',
    'g(x) = 2x + 1 er kommet til i algebravinduet, og der er stadig kun '
    'én linje at se i grafikvinduet. Den grønne ligger under den grå.')]),

 ('Regn en værdi ud',
  ['Skal du vide, hvad noget koster ved et bestemt x — 7 timer, 12 GB — så '
   'skriver du bare tallet i parentesen.',
   'Det svarer til at sætte tallet ind i forskriften i hånden: '
   f'2 · {VAERDI_X} + 1 = {VAERDI_Y}. Gør gerne begge dele; GeoGebra er god '
   'til at fange regnefejl.'],
  [(f'g({VAERDI_X})', 'Svaret står med det samme i algebravinduet')],
  None, None,
  [('11-vaerdi.png',
    f'Nederst i algebravinduet står svaret: {VAERDI_Y}. Det er den '
    f'y-værdi, grafen har ved x = {VAERDI_X}.')]),

 ('Find nulpunktet med kommandoen Rod',
  ['Nulpunktet er dér, hvor grafen rammer <b>x-aksen</b> — hvor y er nul. '
   'Det er fx dér, hvor telefonen er løbet tør for strøm.',
   'Kommandoen hedder <b>Rod</b>. Ikke «Nulpunkt» — det findes ikke i '
   'GeoGebra, selv om det er det, vi kalder det i timen.',
   '<b>Den virker kun på en funktion.</b> Har du kun linjen '
   '<code class="inl">f</code> fra Linje-kommandoen, får du ingenting. '
   'Brug din egen <code class="inl">g</code> fra trin 6.'],
  [('Rod(g)', 'Punktet, hvor grafen krydser x-aksen')],
  None, None,
  [('7-rod.png',
    'Punktet er sat på x-aksen, og koordinaterne står i algebravinduet. '
    'Her er y nul — det er dét, nulpunkt betyder.')]),

 ('To linjer og skæringspunktet',
  ['I opgave D er der to abonnementer. Skriv begge forskrifter som '
   'funktioner, og find så punktet, hvor de krydser hinanden.',
   'Skæringspunktet er det sted, hvor de to koster <b>det samme</b>. Til '
   'venstre for punktet er den ene billigst, til højre den anden. Det er '
   'hele pointen i opgaven.'],
  [('g(x)=2x+1', 'Den første linje'),
   ('h(x)=x+4', 'Den anden linje'),
   ('Skæring(g,h)', 'Punktet, hvor de krydser, med begge koordinater')],
  FIG_SKAER,
  'Skæringspunktet S er dér, hvor de to linjer møder hinanden. '
  'Koordinaterne fortæller både ved hvilket x og til hvilken pris.',
  [('8-skaering.png',
    f'Begge linjer er tegnet, og skæringspunktet står som S = '
    f'({SKAER[0]}, {SKAER[1]}) i algebravinduet.')]),

 ('Få billedet ind i Word',
  ['Opgaven siger, at udregningerne skal laves i Word, og at du skal vise '
   'din metode. Billedet fra GeoGebra <b>er</b> en del af metoden.',
   'Klik på de tre streger øverst til højre → <b>Fil</b> → '
   '<b>Eksporter billede</b>. Så kan du hente billedet og sætte det ind i '
   'Word.',
   '<b>Skriv altid under billedet, hvad x og y står for.</b> Et '
   'koordinatsystem uden enheder siger ingenting — er det timer og kroner, '
   'eller GB og kroner?'],
  [], None, None,
  [('10-menu.png',
    'Menuen, når du har klikket på de tre streger og derefter på Fil. '
    'Eksporter billede er den, du skal bruge.')]),
]

# Punkt for punkt. Hvert punkt er ÉN ting at goere, i den raekkefoelge de
# skal goeres. Det sidste punkt er det vigtigste: funktionen skal bruges
# til noget bagefter.
TJEKLISTE = [
 'Åbn <b>geogebra.org/classic</b>, og vælg <b>Graf</b> i listen.',
 'Skriv dit første punkt, fx <code class="inl">A=(1,3)</code>, og tryk Enter.',
 'Skriv dit andet punkt, fx <code class="inl">B=(4,9)</code>, og tryk Enter.',
 'Skriv <code class="inl">Linje(A,B)</code>. Nu er linjen tegnet.',
 'Skriv ligningen om, så der står <code class="inl">y = ax + b</code>. '
 'Flyt leddet over, og skift fortegn. Det gør du på papiret — du retter '
 '<b>ikke</b> i den linje, der står i GeoGebra.',
 'Skriv <code class="inl">Hældning(f)</code> på en ny linje, og skriv '
 'tallet <code class="inl">a</code> ned. Kig på trappetrinnet, og tæl '
 'efter: 1 til højre, hvor mange op?',
 'Aflæs <code class="inl">b</code> dér, hvor linjen krydser y-aksen, og '
 'skriv tallet ned.',
 'Skriv din egen forskrift: <code class="inl">g(x)=</code> og så dit a og '
 'dit b. Tjek, at den lægger sig oven på linjen.',
 'Tag et billede: tre streger → Fil → Eksporter billede. Sæt det ind i '
 'Word, og skriv under det, hvad x og y står for.',
 '<b>Arbejd videre med den funktion, du nu har lavet.</b> Den er ikke et '
 'mål i sig selv — den er værktøjet. Brug den til at svare på det, '
 'opgaven spørger om: regn en værdi ud med '
 '<code class="inl">g(tal)</code>, find nulpunktet med '
 '<code class="inl">Rod(g)</code>, og læg den anden linje ind, hvis '
 'opgaven har to. Skriv hver gang med ord, hvad tallet betyder i '
 'virkeligheden.',
]

OPGAVER = [
 ('Opgave C · kajakudlejningen og batteriet',
  ['De to kvitteringer er dine to punkter. Sæt dem ind (trin 2), tegn '
   'linjen (trin 3) og skriv ligningen om (trin 4).',
   'Find hældningen (trin 5), aflæs b, og skriv forskriften (trin 6).',
   'Hvad 7 timer koster, finder du med trin 7.',
   'I batteridelen skal du finde nulpunktet — det er trin 8. Læg mærke '
   'til, at a bliver <b>negativ</b> her. Trappetrinnet peger nedad.']),
 ('Opgave D · de to abonnementer',
  ['Her er linjerne tegnet i forvejen. Du skal aflæse a og b og vise ved '
   'regning, at det passer.',
   'Skriv de to forskrifter, du har aflæst, ind som funktioner (trin 9). '
   'Lægger de sig oven i de to tegnede linjer, har du aflæst rigtigt.',
   'Find skæringspunktet med trin 9. Sammenlign med det, du aflæste på '
   'figuren — og med det, du får ved at sætte de to forskrifter lig '
   'hinanden i hånden.',
   'Prisen ved 12 GB hos hver af dem er to gange trin 7.']),
]

FALDER = [
 ('Komma og punktum', 'Koordinater skilles med komma: '
  '<code class="inl">(2,200)</code>. Decimaltal skrives med punktum: '
  '<code class="inl">2.5</code>.'),
 ('Ligningen ser forkert ud', 'GeoGebra skriver '
  '<code class="inl">-2x + y = 1</code> i stedet for '
  '<code class="inl">y = 2x + 1</code>. Det er den samme linje — se trin 4.'),
 ('Linjen er ikke en funktion', '<code class="inl">Linje(A,B)</code> laver en '
  'linje, ikke en funktion. <code class="inl">Rod</code> og '
  '<code class="inl">g(7)</code> virker kun på noget, du har skrevet som '
  '<code class="inl">g(x)=</code>.'),
 ('Du kan ikke se noget', 'Punkterne i opgaverne har store y-værdier — 200, '
  '350. Rul ud med musehjulet, eller brug forstørrelsesglasset nede til '
  'højre, indtil punkterne er inde i billedet.'),
 ('Det hedder Rod', 'Ikke Nulpunkt. Begynd at skrive <b>Rod</b>, så '
  'foreslår GeoGebra resten selv.'),
]

for _t in TRIN:
    for _f, _ in _t[5]:
        assert os.path.exists(os.path.join(ROD, BILLEDER, _f)), \
            f'{_f} mangler — kør claude/hent_geogebra_billeder.mjs'

trin_html = ''
for i, (o, stykker, skriv, figur, figtekst, billeder) in enumerate(TRIN, 1):
    trin_html += (f'<section class="trin"><h2><span class="num">{i}</span>'
                  f'{html.escape(o)}</h2>')
    trin_html += ''.join(
        t if t.startswith('<div') else f'<p>{t}</p>' for t in stykker)
    if skriv:
        trin_html += '<table class="skriv"><tbody>' + ''.join(
            f'<tr><td class="kmd"><code>{html.escape(k)}</code></td>'
            f'<td class="sker">{html.escape(v)}</td></tr>' for k, v in skriv
        ) + '</tbody></table>'
    if figur:
        krop = fig_flyt() if figur == 'FLYT' else figur
        trin_html += (f'<div class="figur">{krop}'
                      f'<div class="figtekst">{html.escape(figtekst)}</div>'
                      f'</div>')
    for fil, tekst in billeder:
        trin_html += (f'<figure class="skaerm">'
                      f'<img src="{BILLEDER}/{fil}" alt="{html.escape(tekst)}" '
                      f'loading="lazy">'
                      f'<figcaption>{html.escape(tekst)}</figcaption></figure>')
    trin_html += '</section>'

tjek_html = ''.join(f'<li><span class="boks"></span><div>{t}</div></li>'
                    for t in TJEKLISTE)
opg_html = ''.join(
    f'<div class="opg"><h3>{html.escape(o)}</h3>'
    + ''.join(f'<p>{t}</p>' for t in stykker) + '</div>' for o, stykker in OPGAVER)
falder_html = ''.join(
    f'<tr><th>{html.escape(a)}</th><td>{b}</td></tr>' for a, b in FALDER)

BASIS = open('funktioner-og-ligninger.html', encoding='utf-8').read()
CSS = BASIS[BASIS.find('<style>') + 7:BASIS.find('</style>')]
CSS += '''
.trin{background:var(--panel,#fff);border:1px solid var(--line);
border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;
margin:16px 0}
.trin h2{font-size:1.18rem;margin:0 0 10px;display:flex;align-items:center;
gap:12px}
.trin .num{width:30px;height:30px;border-radius:9px;display:grid;
place-items:center;font-weight:800;font-size:.95rem;background:var(--accent);
color:#fff;flex:0 0 auto}
.trin p{margin:8px 0;color:var(--muted);font-size:.97rem;max-width:72ch}
.trin p b{color:var(--ink)}
table.skriv{width:100%;border-collapse:collapse;margin:14px 0}
table.skriv td{border:1px solid var(--line);padding:9px 12px;
vertical-align:middle}
table.skriv td.kmd{width:40%;background:#1a2233;border-color:#1a2233}
table.skriv td.kmd code{color:#eaf0ff;font-size:1.02rem;font-weight:700}
table.skriv td.sker{color:var(--muted);font-size:.93rem}
.ikon{width:1.3em;height:1.3em;vertical-align:-.3em;margin:0 1px}
.ikonboks{display:flex;gap:12px;align-items:flex-start;
background:var(--panel2);border:1px solid var(--line);border-radius:12px;
padding:12px 16px;margin:12px 0}
.ikonboks>.ikon{width:26px;height:26px;flex:0 0 auto;margin:2px 0 0}
.ikonboks p{margin:0;color:var(--muted);font-size:.95rem;max-width:66ch}
.advarsel{display:flex;gap:12px;align-items:flex-start;background:#fff7ef;
border:1px solid #f0d9c0;border-left:5px solid #d98324;border-radius:12px;
padding:13px 17px;margin:4px 0 14px}
.advarsel>.ikon{width:26px;height:26px;flex:0 0 auto;margin:1px 0 0}
.advarsel p{margin:0;color:var(--muted);font-size:.97rem;max-width:66ch}
.advarsel b{color:var(--ink)}
figure.skaerm{margin:14px 0;border:1px solid var(--line);border-radius:12px;
overflow:hidden;background:#fff}
/* Et hoejt, smalt skaermbillede (app-listen) maa ikke fylde en
   hel skaerm, naar et bredt kun fylder en tredjedel. */
figure.skaerm img{display:block;max-width:100%;max-height:430px;
width:auto;height:auto;margin:0 auto}
figure.skaerm figcaption{padding:10px 14px;background:var(--panel2);
color:var(--muted);font-size:.88rem;border-top:1px solid var(--line)}
svg.flyt{width:100%;max-width:520px;height:auto;display:block;margin:0 auto}
ol.tjek{list-style:none;counter-reset:t;padding:0;margin:14px 0}
ol.tjek li{counter-increment:t;display:flex;gap:14px;align-items:flex-start;
background:var(--panel,#fff);border:1px solid var(--line);border-radius:12px;
padding:12px 16px;margin:8px 0;break-inside:avoid}
ol.tjek li::before{content:counter(t);flex:0 0 auto;width:26px;height:26px;
border-radius:8px;background:var(--accent);color:#fff;font-weight:800;
font-size:.85rem;display:grid;place-items:center}
ol.tjek .boks{flex:0 0 auto;width:20px;height:20px;border-radius:5px;
border:2px solid var(--line);margin-top:3px}
ol.tjek div{color:var(--muted);font-size:.97rem;max-width:68ch}
ol.tjek div b{color:var(--ink)}
.opg{background:var(--panel2);border:1px solid var(--line);border-radius:12px;
padding:14px 20px;margin:14px 0}
.opg h3{margin:0 0 6px;font-size:1.05rem}
.opg p{margin:6px 0;color:var(--muted);font-size:.95rem;max-width:72ch}
table.falder{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.falder th,table.falder td{border:1px solid var(--line);padding:10px 12px;
text-align:left;vertical-align:top}
table.falder th{background:var(--panel2);width:30%}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:10px;text-align:left;
max-width:66ch;margin-left:auto;margin-right:auto}
h2.sec{font-size:1.4rem;margin:30px 0 6px}
.kilde{color:var(--muted);font-size:.85rem;margin:18px 0 0}
@media print{header.top,.printbtn,.btn{display:none!important}
.trin,.figur,.opg,figure.skaerm,ol.tjek li{break-inside:avoid;
page-break-inside:avoid}
figure.skaerm img{max-height:88mm;width:auto}
body{font-size:11pt}main{padding:0}@page{size:A4;margin:14mm}}
'''

KROP = f'''<section class="hero">
<span class="pill">Matematik · lineære funktioner</span>
<h1>Intro til GeoGebra</h1>
<p>Ti trin, der dækker præcis det, du skal bruge i <b>opgave C og D</b>.
Alle eksempler bruger andre tal end opgaverne — fremgangsmåden er den samme,
men svarene skal du selv finde. Hvert trin har et billede af, hvordan det
ser ud på skærmen.</p>
<button class="printbtn" onclick="window.print()">Print vejledningen</button>
<a class="btn" href="{GEOGEBRA}" target="_blank" rel="noopener">Åbn GeoGebra</a>
<a class="btn ghost" href="funktioner-og-ligninger.html">Tilbage til opgaverne</a>
</section>
<div id="trin">{trin_html}</div>
<h2 class="sec" id="punktforpunkt">Punkt for punkt — sådan gør du</h2>
<p style="color:var(--muted);max-width:72ch">Ét punkt ad gangen, i den
rækkefølge de står. Sæt et kryds, når du er færdig med et punkt.</p>
<ol class="tjek">{tjek_html}</ol>
<h2 class="sec" id="opgaver">Sådan bruger du trinnene i opgaverne</h2>
{opg_html}
<h2 class="sec" id="falder">Fem ting, der driller</h2>
<table class="falder"><tbody>{falder_html}</tbody></table>
<p class="kilde">Skærmbillederne er fra GeoGebra Classic, geogebra.org.</p>
<button class="printbtn" onclick="window.print()">Print vejledningen</button>'''

DOK = ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1">'
       '<title>Intro til GeoGebra · 9. klasse</title><style>'
       + CSS + '</style></head><body><header class="top"><div class="top-inner">'
       '<div class="brand">321flyv · <span>Intro til GeoGebra</span>'
       '</div><nav class="jump">'
       '<a href="#trin">Trinnene</a><a href="#punktforpunkt">Punkt for punkt</a>'
       '<a href="#opgaver">I opgaverne</a><a href="#falder">Det der driller</a>'
       '<a href="funktioner-og-ligninger.html">Opgaverne</a>'
       '</nav></div></header><main>' + KROP + '</main><footer>'
       'Undervisningsmateriale · 9. klasse.</footer></body></html>')

open(UD, 'w', encoding='utf-8').write(DOK)
print(f'skrevet:  {UD}  ·  {len(TRIN)} trin, '
      f'{sum(len(t[5]) for t in TRIN)} skærmbilleder, '
      f'{sum(1 for t in TRIN if t[3])} tegnede figurer, '
      f'{len(TJEKLISTE)} punkter i tjeklisten')
