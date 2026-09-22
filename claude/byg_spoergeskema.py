# -*- coding: utf-8 -*-
"""Bygger spørgeskema-projektet "Ung i Tyskland".

Ét spørgeskema (Google Forms), ens for alle unger. Hver ung får sin egen
adresse på sitet, www.mibelibsen.space/u/<kode>, som sender videre til
spørgeskemaet med ungens navn forudfyldt i et skjult felt. Så tæller hvert
svar på den ung, hvis QR-kode blev scannet — og alle svar lander i det samme
regneark.

Læser:
    spoergeskema/opsaetning.json   site, link til spørgeskemaet (med NAVN som
                                   pladsholder) og link til forslagsformularen
    spoergeskema/unger.txt         ét navn pr. linje, # er kommentar

Skriver:
    vercel.json                    redirects /u/<kode> → spørgeskemaet
    tysk-spoergeskema.html         siden til ungerne
    spoergeskema/unger-links.tsv   navn, kode og links — til fanen "Unger"
    spoergeskema/qr-plakater-a4.pdf   én A4-plakat pr. ung
    spoergeskema/qr-kort-a6.pdf       fire A6-kort pr. ark, til at klippe ud
    spoergeskema/eksempel-plakat.pdf  en plakat med et opdigtet navn

Mappen spoergeskema/ er udelukket fra deploy — navnene hører ikke på sitet.
Kun koderne (/u/anna) står i vercel.json, og de er alligevel trykt på plakaterne.

Kør:  python3 claude/byg_spoergeskema.py
"""
import html
import json
import os
import re
import subprocess
import sys
import unicodedata
from urllib.parse import quote

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROD)
sys.path.insert(0, 'claude')
import figurer as FG   # noqa: E402
import qr              # noqa: E402

SIDE = 'tysk-spoergeskema.html'
MAPPE = 'spoergeskema'
OPS = json.load(open(f'{MAPPE}/opsaetning.json', encoding='utf-8'))
SITE = OPS['site'].rstrip('/')
FORMULAR = OPS.get('formular', '').strip()
FORSLAG = OPS.get('forslag', '').strip()
FORSLAG_CSV = OPS.get('forslag_csv', '').strip()      # fanen Forslag, udgivet som CSV
FORSLAG_LISTE = OPS.get('forslag_liste', '').strip()  # samme fane som webside
EKSEMPEL = ('Freja Eksempel', 'eksempel')
if FORMULAR:
    assert 'NAVN' in FORMULAR, ('linket til spørgeskemaet skal have NAVN dér, hvor '
                                'ungens navn skal ind — se vejledningen')


# ------------------------------------------------------------------ unger
def kode(navn):
    """anna-k af "Anna K." — kun a-z, 0-9 og bindestreg, så adressen kan tastes."""
    s = navn.lower()
    for a, b in (('æ', 'ae'), ('ø', 'oe'), ('å', 'aa'), ('ä', 'ae'), ('ö', 'oe'),
                 ('ü', 'ue'), ('ß', 'ss')):
        s = s.replace(a, b)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    assert s, f'kan ikke lave en kode af navnet {navn!r}'
    return s


def laes_unger():
    unger = []
    if os.path.exists(f'{MAPPE}/unger.txt'):
        for linje in open(f'{MAPPE}/unger.txt', encoding='utf-8'):
            navn = linje.split('#', 1)[0].strip()
            if navn:
                unger.append((navn, kode(navn)))
    koder = [k for _, k in unger]
    for k in set(koder):
        if koder.count(k) > 1:
            navne = [n for n, kk in unger if kk == k]
            sys.exit(f'FEJL: {navne} giver samme kode "{k}". Skriv fx efternavnets '
                     f'forbogstav på: "Anna K." og "Anna S."')
    assert EKSEMPEL[1] not in koder, 'koden "eksempel" er reserveret'
    return unger


def qr_adresse(k):
    return f'{SITE}/u/{k}'


def formular_adresse(navn):
    return FORMULAR.replace('NAVN', quote(navn)) if FORMULAR else f'{SITE}/{SIDE}'


# ------------------------------------------------------------- vercel.json
def skriv_redirects(unger):
    v = json.load(open('vercel.json', encoding='utf-8'))
    andre = [r for r in v.get('redirects', []) if not r['source'].startswith('/u/')]
    nye = [{'source': f'/u/{EKSEMPEL[1]}', 'destination': f'{SITE}/{SIDE}',
            'permanent': False}]
    for navn, k in unger:
        nye.append({'source': f'/u/{k}', 'destination': formular_adresse(navn),
                    'permanent': False})
    v['redirects'] = andre + nye
    json.dump(v, open('vercel.json', 'w', encoding='utf-8'), indent=2,
              ensure_ascii=False)
    open('vercel.json', 'a').write('\n')
    return len(nye)


# ------------------------------------------------------------- plakaterne
OVERSKRIFT = 'Wie ist es, jung in Deutschland zu sein?'
UNDERTITEL = 'Umfrage einer 9. Klasse aus Dänemark'
TEKST = ('Hallo! Ich heiße {fornavn} und gehe in Dänemark in die 9. Klasse. '
         'Meine Klasse sammelt Wissen darüber, wie es ist, in Deutschland jung '
         'zu sein. Das vergleichen wir damit, wie es ist, in Dänemark jung zu '
         'sein. Scanne bitte den QR-Code und beantworte unseren Fragebogen. '
         'Es dauert nur ein paar Minuten, und alle Antworten sind anonym. '
         'Vielen Dank!')
TAK = 'Danke, dass du mitmachst!'


def dannebrog(h=14):
    """Dannebrog i de rigtige proportioner: 12-4-21 på langs, 12-4-12 på tværs."""
    w = h * 37 / 28
    e = h / 28
    return (f'<svg viewBox="0 0 37 28" width="{w:.1f}" height="{h}" '
            f'role="img" aria-label="Dannebrog" style="vertical-align:-2px">'
            f'<rect width="37" height="28" fill="#c8102e"/>'
            f'<rect x="12" width="4" height="28" fill="#fff"/>'
            f'<rect y="12" width="37" height="4" fill="#fff"/></svg>')


def plakat(navn, k, klasse='plakat'):
    fornavn = navn.split()[0]
    adresse = qr_adresse(k)
    kort = adresse.replace('https://', '')
    return (f'<div class="{klasse}">'
            f'<div class="top">{html.escape(UNDERTITEL)}</div>'
            f'<h1>{html.escape(OVERSKRIFT)}</h1>'
            f'<div class="qr">{qr.svg(adresse, ec="Q", mm=100)}</div>'
            f'<div class="navn">{html.escape(navn)}</div>'
            f'<div class="sub">{dannebrog()} 9. Klasse · Dänemark</div>'
            f'<p class="tekst">{html.escape(TEKST.format(fornavn=fornavn))}</p>'
            f'<div class="url">Oder im Browser: <b>{html.escape(kort)}</b></div>'
            f'<div class="fod">{html.escape(TAK)}</div>'
            f'</div>')


CSS_PLAKAT = '''
*{box-sizing:border-box}
body{margin:0;font-family:"Liberation Sans",Arial,Helvetica,sans-serif;color:#1a2233}
.plakat{display:flex;flex-direction:column;align-items:center;text-align:center}
.plakat .top{font-size:11pt;letter-spacing:.8px;text-transform:uppercase;color:#1f6fd6;font-weight:700}
.plakat h1{font-size:25pt;line-height:1.15;margin:3mm 0 8mm;max-width:160mm}
.plakat .qr{border:1.2mm solid #1a2233;border-radius:6mm;padding:5mm;background:#fff}
.plakat .qr svg{display:block;width:100mm;height:100mm}
.plakat .navn{font-size:30pt;font-weight:800;margin-top:8mm;line-height:1.1}
.plakat .sub{color:#586074;font-size:13pt;margin:2mm 0 7mm}
.plakat .tekst{font-size:13pt;line-height:1.45;max-width:152mm;margin:0}
.plakat .url{margin-top:auto;font-size:12.5pt;border:1px solid #d3dae7;border-radius:3mm;padding:2.5mm 6mm;color:#586074}
.plakat .url b{color:#1a2233;font-family:"Liberation Mono","DejaVu Sans Mono",monospace}
.plakat .fod{font-size:10pt;color:#586074;margin-top:4mm}
'''

CSS_A4 = CSS_PLAKAT + '''
@page{size:A4;margin:0}
.side{width:210mm;height:297mm;padding:16mm 18mm 14mm;page-break-after:always;display:flex}
.side:last-child{page-break-after:auto}
.side .plakat{flex:1}
'''

CSS_A6 = CSS_PLAKAT + '''
@page{size:A4;margin:0}
.ark{width:210mm;height:297mm;display:grid;grid-template-columns:105mm 105mm;grid-template-rows:148.5mm 148.5mm;page-break-after:always}
.ark:last-child{page-break-after:auto}
.kort{padding:8mm 8mm 6mm;border:0.3mm dashed #9aa6ba;display:flex}
.kort .plakat{flex:1}
.plakat .top{font-size:7pt}
.plakat h1{font-size:12.5pt;margin:1.5mm 0 3mm;max-width:85mm}
.plakat .qr{border-width:0.7mm;border-radius:3mm;padding:2.5mm}
.plakat .qr svg{width:50mm;height:50mm}
.plakat .navn{font-size:15pt;margin-top:3mm}
.plakat .sub{font-size:8pt;margin:1mm 0 2.5mm}
.plakat .tekst{font-size:7.6pt;line-height:1.38;max-width:86mm}
.plakat .url{font-size:7pt;padding:1.2mm 3mm;border-radius:1.5mm;margin-top:auto}
.plakat .fod{font-size:6.5pt;margin-top:1.5mm}
'''


def html_dok(titel, css, krop):
    return (f'<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8">'
            f'<title>{html.escape(titel)}</title><style>{css}</style></head>'
            f'<body>{krop}</body></html>')


def pdf(kilde_html, ud_pdf, png=None):
    args = ['node', 'claude/html_til_pdf.mjs', kilde_html, ud_pdf] + ([png] if png else [])
    subprocess.run(args, check=True)


def sider_i_pdf(sti):
    # Chromiums PDF'er har sideobjekterne ukomprimeret, saa de kan taelles
    return len(re.findall(rb'/Type\s*/Page[^s]', open(sti, 'rb').read()))


def skriv_plakater(unger, scratch):
    os.makedirs(scratch, exist_ok=True)
    # eksemplet — altid, ogsaa uden navne
    k = f'{scratch}/eksempel.html'
    open(k, 'w', encoding='utf-8').write(html_dok(
        'Eksempel', CSS_A4, f'<div class="side">{plakat(*EKSEMPEL)}</div>'))
    pdf(k, f'{MAPPE}/eksempel-plakat.pdf', f'{scratch}/eksempel.png')
    if not unger:
        return
    sider = ''.join(f'<div class="side">{plakat(n, kk)}</div>' for n, kk in unger)
    k = f'{scratch}/a4.html'
    open(k, 'w', encoding='utf-8').write(html_dok('QR-plakater', CSS_A4, sider))
    pdf(k, f'{MAPPE}/qr-plakater-a4.pdf')
    n = sider_i_pdf(f'{MAPPE}/qr-plakater-a4.pdf')
    assert n == len(unger), f'A4: {n} sider i PDF, men {len(unger)} unger'
    ark = []
    for i in range(0, len(unger), 4):
        kort = ''.join(f'<div class="kort">{plakat(n, kk)}</div>'
                       for n, kk in unger[i:i + 4])
        ark.append(f'<div class="ark">{kort}</div>')
    k = f'{scratch}/a6.html'
    open(k, 'w', encoding='utf-8').write(html_dok('QR-kort', CSS_A6, ''.join(ark)))
    pdf(k, f'{MAPPE}/qr-kort-a6.pdf', f'{scratch}/a6.png')
    n = sider_i_pdf(f'{MAPPE}/qr-kort-a6.pdf')
    assert n == len(ark), f'A6: {n} sider i PDF, men {len(ark)} ark'


def skriv_tsv(unger):
    linjer = ['Navn\tKode\tQR-link\tSpørgeskemaet med navnet i']
    for navn, k in unger:
        linjer.append(f'{navn}\t{k}\t{qr_adresse(k)}\t{formular_adresse(navn)}')
    open(f'{MAPPE}/unger-links.tsv', 'w', encoding='utf-8').write('\n'.join(linjer) + '\n')


# --------------------------------------------------------- kontrol af QR
def tjek_qr(unger):
    """Hver kode læses tilbage med zxing-cpp, hvis det er installeret."""
    try:
        import numpy
        import zxingcpp
    except ImportError:
        print('  (zxing-cpp er ikke installeret — QR-koderne er ikke læst tilbage; '
              'pip install zxing-cpp numpy)')
        return
    for _, k in [EKSEMPEL] + unger:
        adresse = qr_adresse(k)
        m, v, _ = qr.matrix(adresse, 'Q')
        n = len(m)
        px = numpy.full(((n + 8) * 5, (n + 8) * 5), 255, dtype=numpy.uint8)
        for y in range(n):
            for x in range(n):
                if m[y][x]:
                    px[(y + 4) * 5:(y + 5) * 5, (x + 4) * 5:(x + 5) * 5] = 0
        r = zxingcpp.read_barcode(px)
        assert r is not None and r.text == adresse, f'QR for {k} kunne ikke læses'
    print(f'  {len(unger) + 1} QR-koder læst tilbage med zxing-cpp')


# ------------------------------------------------------------------ siden
CSS_SIDE = '''
:root{--bg:#fff;--panel:#fff;--panel2:#f4f6fb;--ink:#1a2233;--muted:#586074;--line:#d3dae7;--accent:#1f6fd6;--accent-soft:#eaf2fd;--good:#1a8f5e;--warn:#b5710a;--shadow:0 1px 3px rgba(20,30,60,.08)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}
header.top{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-inner{max-width:1040px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{font-weight:800;font-size:1.05rem;text-decoration:none;color:var(--ink)}
.brand span{color:var(--accent)}
nav.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
nav.tabs a,nav.tabs span{font-size:.86rem;padding:6px 12px;border-radius:999px;border:1px solid transparent;text-decoration:none;color:var(--muted)}
nav.tabs a:hover{color:var(--ink);border-color:var(--line);background:var(--panel2)}
nav.tabs a.active{background:var(--accent);color:#fff}
nav.tabs span.soon{color:#9aa6ba;cursor:default}
main{max-width:1040px;margin:0 auto;padding:28px 20px 90px}
.hero{background:var(--panel2);border:1px solid var(--line);border-radius:20px;padding:32px;box-shadow:var(--shadow);margin-bottom:20px}
.hero h1{margin:0 0 8px;font-size:2rem}
.hero p{margin:0 0 10px;color:var(--muted);max-width:70ch}
.pill{display:inline-block;font-size:.74rem;letter-spacing:.6px;text-transform:uppercase;color:var(--accent);border:1px solid var(--line);border-radius:999px;padding:4px 12px;margin-bottom:12px;background:#fff;font-weight:700}
h2.sec{font-size:1.5rem;margin:28px 0 6px;display:flex;align-items:center;gap:12px}
.num{width:36px;height:36px;border-radius:10px;display:grid;place-items:center;font-weight:800;background:var(--accent);color:#fff;flex:0 0 auto}
.note{background:var(--panel2);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:14px 18px;margin:16px 0}
.note.gul{border-left-color:var(--warn);background:#fff7e9}
.btnlink{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;text-decoration:none;padding:10px 18px;border-radius:10px;font-weight:700;font-size:.95rem;margin:6px 8px 0 0}
.btnlink.ghost{background:#fff;color:var(--ink);border:1px solid var(--line)}
.btnlink.ghost:hover{border-color:var(--accent);color:var(--accent)}
footer{max-width:1040px;margin:0 auto;padding:0 20px 60px;color:var(--muted);font-size:.85rem;text-align:center}
.figur{background:var(--panel2);border:1px solid var(--line);border-radius:14px;padding:16px;margin:16px 0;text-align:center}
.figur svg{max-width:100%;height:auto}
.figtekst{color:var(--muted);font-size:.9rem;margin-top:8px}
.blok{background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:14px;padding:18px 22px;margin:14px 0;box-shadow:var(--shadow)}
.blok.gron{border-left-color:var(--good)}
.blok h3{margin:0 0 8px;font-size:1.15rem}
.blok p,.blok li{color:var(--muted);font-size:.97rem}
.blok p{margin:6px 0;max-width:74ch}
.blok ul{margin:6px 0;padding-left:20px}
table.t{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
table.t th,table.t td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
table.t th{background:var(--panel2)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:8px;align-items:start}
@media(max-width:720px){.two{grid-template-columns:1fr}}
iframe.form{width:100%;height:900px;border:1px solid var(--line);border-radius:14px;background:#fff}
/* plakaten som den ser ud paa papir, skaleret ned */
.plakat{max-width:360px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 20px;display:flex;flex-direction:column;align-items:center;text-align:center;box-shadow:var(--shadow)}
.plakat .top{font-size:.66rem;letter-spacing:.8px;text-transform:uppercase;color:var(--accent);font-weight:700}
.plakat h1{font-size:1.15rem;line-height:1.2;margin:4px 0 12px}
.plakat .qr{border:3px solid var(--ink);border-radius:12px;padding:8px;background:#fff}
.plakat .qr svg{display:block;width:170px;height:170px}
.plakat .navn{font-size:1.5rem;font-weight:800;margin-top:12px;line-height:1.1}
.plakat .sub{color:var(--muted);font-size:.85rem;margin:2px 0 10px}
.plakat .tekst{font-size:.78rem;line-height:1.45;margin:0;color:var(--ink)}
.plakat .url{margin-top:12px;font-size:.74rem;border:1px solid var(--line);border-radius:8px;padding:5px 10px;color:var(--muted)}
.plakat .url b{color:var(--ink);font-family:Consolas,monospace}
.plakat .fod{font-size:.7rem;color:var(--muted);margin-top:8px}
.liste{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:12px 0}
.forslag{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:var(--shadow)}
.forslag .hvem{font-weight:800;margin-bottom:6px}
.forslag .felt{font-size:.92rem;margin:4px 0}
.forslag .felt span{color:var(--muted);font-size:.8rem;display:block}
.tom{color:var(--muted);font-style:italic}
@media print{header.top,.btnlink,iframe.form{display:none!important}.hero,.blok,.figur,.plakat{box-shadow:none;break-inside:avoid}body{color:#000}@page{size:A4;margin:13mm}}
'''


def figur_proces():
    trin = [
        ('I foreslår spørgsmål',
         'Skriv dit spørgsmål på tysk i formularen. Alle forslag lander i ét regneark.', 'jer'),
        ('Vi vælger og retter sproget',
         'Klassen vælger de bedste spørgsmål, og vi retter tysken sammen.', 'os'),
        ('Spørgeskemaet bygges',
         'Ét spørgeskema, ens for alle. Det kan besvares på en telefon på et par minutter.', 'os'),
        ('Du får din egen QR-kode',
         'Koden fører til det fælles spørgeskema — men den husker, at det er dig, der har skaffet svaret.', 'jer'),
        ('Tyske unge svarer',
         'Vis koden frem. Under den står dit navn og en tysk tekst om, hvad vi undersøger.', 'de'),
        ('Alle svar samles',
         'Ét regneark med alle svar — og en optælling af, hvor mange hver af jer har skaffet.', 'os'),
    ]
    farver = {'jer': FG.BLA, 'os': FG.GRO, 'de': FG.ORA}
    return FG.procesdiagram(trin, farver=farver,
                            legende=(('Det gør du', 'jer'), ('Det gør vi sammen', 'os'),
                                     ('Det sker i Tyskland', 'de')))


def figur_cirkel():
    dele = [('Unter 2 Stunden', 5), ('2–4 Stunden', 9), ('Mehr als 4 Stunden', 6)]
    from fractions import Fraction as F
    N = sum(v for _, v in dele)
    assert sum(F(v, N) * 100 for _, v in dele) == 100
    assert sum(F(v, N) * 360 for _, v in dele) == 360
    return FG.cirkeldiagram(dele)


def figur_optaelling():
    vals = [7, 12, 4, 9, 15, 6]
    kats = ['A', 'B', 'C', 'D', 'E', 'F']
    return FG.soejler(vals, kats, titel=f'Svar pr. ung — {sum(vals)} svar i alt',
                      ynavn='Antal svar')


def liste_html():
    """Sektionen 'Jeres spørgsmål': siden henter fanen Forslag som CSV, hver gang
    den åbnes, og viser hvert forslag som et kort. Tidsstempel og e-mail vises
    ikke. Kolonnerne følger formularens spørgsmål, så nye felter kommer med af
    sig selv. Kan CSV'en ikke hentes, vises et link til listen i Google."""
    aabn = (f'<a class="btnlink ghost" href="{html.escape(FORSLAG_LISTE)}" target="_blank" '
            f'rel="noopener">Åbn arket</a>' if FORSLAG_LISTE else '')
    return f"""<div class="blok gron" id="jeres"><h3>Jeres spørgsmål indtil nu <span id="antal"></span></h3>
<p>Listen hentes fra det fælles regneark, hver gang siden åbnes. Nye spørgsmål står her et øjeblik efter, at de er skrevet ind.</p>
<div class="liste" id="liste"><p class="tom">Henter forslagene …</p></div>
{aabn}</div>
<script>
(function(){{
  var URL = {json.dumps(FORSLAG_CSV)};
  var SKJUL = /^(timestamp|tidsstempel|email address|e-mailadresse|mailadresse)$/i;
  function csv(t){{           // felter i anførselstegn kan have komma og linjeskift
    var rows=[], row=[], f='', q=false;
    for(var i=0;i<t.length;i++){{
      var c=t[i];
      if(q){{ if(c=='"'){{ if(t[i+1]=='"'){{f+='"';i++;}} else q=false; }} else f+=c; }}
      else if(c=='"') q=true;
      else if(c==','){{row.push(f);f='';}}
      else if(c=='\\n'||c=='\\r'){{ if(c=='\\r'&&t[i+1]=='\\n') i++; row.push(f); rows.push(row); row=[]; f=''; }}
      else f+=c;
    }}
    if(f!==''||row.length){{row.push(f);rows.push(row);}}
    return rows.filter(function(r){{return r.some(function(x){{return x.trim();}});}});
  }}
  function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  var el=document.getElementById('liste'), antal=document.getElementById('antal');
  fetch(URL+'&t='+Date.now(),{{cache:'no-store'}}).then(function(r){{
    if(!r.ok) throw new Error(r.status); return r.text();
  }}).then(function(t){{
    var rows=csv(t); if(!rows.length) throw new Error('tom');
    var hoved=rows[0], data=rows.slice(1).filter(function(r){{return (r[0]||'').trim().toLowerCase()!=='eksempel';}}).reverse();
    var vis=[]; hoved.forEach(function(h,i){{ if(!SKJUL.test(h.trim())) vis.push(i); }});
    antal.textContent='('+data.length+')';
    if(!data.length){{ el.innerHTML='<p class="tom">Ingen forslag endnu. Bliv den første!</p>'; return; }}
    el.innerHTML=data.map(function(r){{
      var hvem=r[vis[0]]||'', felter=vis.slice(1).map(function(i){{
        return r[i]&&r[i].trim()?'<div class="felt"><span>'+esc(hoved[i])+'</span>'+esc(r[i])+'</div>':'';
      }}).join('');
      return '<div class="forslag"><div class="hvem">'+esc(hvem)+'</div>'+felter+'</div>';
    }}).join('');
  }}).catch(function(){{
    el.innerHTML='<p class="tom">Listen kunne ikke hentes lige nu. Prøv knappen herunder.</p>';
  }});
}})();
</script>"""


def skriv_side(unger):
    if FORSLAG:
        forslag_knap = f'<a class="btnlink" href="{html.escape(FORSLAG)}" target="_blank" rel="noopener">Skriv dit spørgsmål i arket</a>'
        forslag_blok = ('<div class="blok"><h3>Sådan skriver du et spørgsmål</h3>'
                        '<p>Spørgsmålene samles i ét fælles regneark, som alle i klassen kan skrive i. '
                        'Åbn arket, find den næste tomme linje, og udfyld: dit navn, spørgsmålet på tysk, '
                        'svartypen og — hvis svartypen er <i>Auswahl</i> — svarmulighederne.</p>'
                        '<p><b>Svartyper:</b> <i>Ja/Nein</i> · <i>Auswahl</i> (flere svar at vælge imellem) · '
                        '<i>Skala 1–5</i> · <i>Zahl</i> (et tal, fx timer eller euro) · <i>Freier Text</i>. '
                        'Husk: kun de fire første kan tælles og tegnes som diagram.</p>'
                        '<p>Ret ikke i andres linjer. Øverst står et eksempel, som ikke tæller med.</p>'
                        f'{forslag_knap}</div>')
    else:
        forslag_knap = ''
        forslag_blok = ('<div class="note gul"><b>Formularen er på vej.</b> Linket til '
                        'forslagsformularen bliver sat ind her, så snart den er lavet. '
                        'Indtil da: skriv dine forslag ned, så de er klar.</div>')
    forslag_liste = liste_html() if FORSLAG_CSV else ''
    status = (f'{len(unger)} unger har fået en kode.' if unger
              else 'Koderne laves, når navnelisten er klar.')
    krop = f'''<header class="top"><div class="top-inner"><a class="brand" href="index.html">Mibelibsen <span>9. klasse</span></a><nav class="tabs"><a class="" href="matematik.html">Matematik</a><a class="" href="samfundsfag.html">Samfundsfag</a><a class="active" href="tysk.html">Tysk</a><span class="soon">Fysik</span></nav></div></header>
<main>
<section class="hero"><span class="pill">Tysk · 9. klasse</span>
<h1>Ung i Tyskland</h1>
<p>Hvordan er det at være ung i Tyskland — og er det anderledes end i Danmark?
Det finder vi ud af med et spørgeskema, som I selv laver spørgsmålene til.
Hver af jer får sin egen QR-kode, og alle svar samles i ét regneark, så vi
kan se, hvem der har skaffet hvor mange.</p>
{forslag_knap}<a class="btnlink ghost" href="tysk.html">Tilbage til tysk</a></section>

<h2 class="sec"><span class="num">1</span>Sådan foregår det</h2>
<div class="figur">{figur_proces()}<div class="figtekst">Seks trin fra jeres forslag til det færdige regneark. Blå er dit, grøn gør vi sammen, orange sker i Tyskland.</div></div>

<h2 class="sec"><span class="num">2</span>Foreslå et spørgsmål</h2>
<div class="two">
<div class="blok"><h3>Det gør et spørgsmål godt</h3>
<ul>
<li><b>Lukkede svar.</b> Giv 2–5 svarmuligheder, man kan krydse af. Så kan svarene tælles og tegnes som diagram. "Hvad synes du om skolen?" kan ikke tælles — "Hvor mange timer laver du lektier om ugen: under 2, 2–5, over 5?" kan.</li>
<li><b>Ét spørgsmål ad gangen.</b> Ikke "sover du nok, og er du træt i skolen?"</li>
<li><b>Skal kunne stilles i Danmark også.</b> Vi stiller de samme spørgsmål til os selv, så vi kan sammenligne.</li>
<li><b>Ikke for privat.</b> Den, der svarer, er en fremmed ung på gaden i Tyskland. Spørg om hverdag, skole, fritid, penge, telefon, venner, fremtid — ikke om ting man ikke vil svare på.</li>
<li><b>Kort og på tysk.</b> Skriv gerne den danske udgave ved siden af, så vi kan stille det samme spørgsmål i Danmark. Vi retter tysken sammen bagefter.</li>
</ul></div>
<div class="blok gron"><h3>Eksempler</h3>
<table class="t"><tr><th>På dansk</th><th>På tysk</th><th>Svar</th></tr>
<tr><td>Hvor mange timer bruger du på din telefon om dagen?</td><td>Wie viele Stunden am Tag bist du am Handy?</td><td>Unter 2 · 2–4 · Mehr als 4</td></tr>
<tr><td>Har du et fritidsjob?</td><td>Hast du einen Nebenjob?</td><td>Ja · Nein</td></tr>
<tr><td>Hvor tit ses du med venner uden for skolen?</td><td>Wie oft triffst du Freunde außerhalb der Schule?</td><td>Jeden Tag · Ein paar Mal pro Woche · Seltener</td></tr>
<tr><td>Hvad bekymrer dig mest lige nu?</td><td>Was macht dir gerade am meisten Sorgen?</td><td>Schule · Geld · Klima · Freunde · Zukunft</td></tr>
<tr><td>Hvor mange timer sover du før en skoledag?</td><td>Wie viele Stunden schläfst du vor einem Schultag?</td><td>Unter 6 · 6–8 · Mehr als 8</td></tr>
</table>
<p>Alder og køn spørger vi altid om til sidst, så vi kan dele svarene op.</p></div>
</div>
<div class="figur">{figur_cirkel()}<div class="figtekst">Sådan bliver et lukket spørgsmål til et diagram: "Wie viele Stunden am Tag bist du am Handy?" med 20 tænkte svar. Frekvenserne giver 100 %, graderne 360°.</div></div>
{forslag_blok}
{forslag_liste}

<h2 class="sec"><span class="num">3</span>Din QR-kode</h2>
<div class="two">
<div>
<div class="blok"><h3>Sådan virker den</h3>
<p>Din kode fører til adressen <b>{html.escape(SITE.replace('https://', ''))}/u/dit-navn</b>. Den sender videre til det fælles spørgeskema med dit navn gemt i linket, så hvert svar tæller på dig. Den, der svarer, ser bare spørgeskemaet.</p>
<p>Under koden står dit navn og en tysk tekst om, hvad vi undersøger — så kan du vise plakaten frem uden at skulle forklare det hele på tysk først.</p>
<p>Du får koden som plakat (A4) og som lille kort, der kan ligge i lommen. Et billede af koden på telefonen virker lige så godt.</p>
<p><b>Prøv at scanne eksemplet.</b> Det fører tilbage hertil.</p></div>
<div class="note"><b>Status:</b> {status}</div>
</div>
{plakat(*EKSEMPEL)}
</div>

<h2 class="sec"><span class="num">4</span>Optællingen</h2>
<p>Hvert svar bliver gemt med navnet fra den kode, der blev scannet. Regnearket tæller selv sammen, så vi hele tiden kan se, hvem der har skaffet hvor mange svar — og hvor mange vi har i alt.</p>
<div class="figur">{figur_optaelling()}<div class="figtekst">Tænkt eksempel på optællingen for seks unger. De rigtige tal kommer fra regnearket.</div></div>

<h2 class="sec"><span class="num">5</span>Når svarene er hjemme</h2>
<div class="blok"><h3>Så bliver det matematik</h3>
<p>Svarene fra Tyskland og jeres egne svar fra Danmark er to datasæt. Dem sammenligner vi med det, I kan fra statistik: frekvenser, cirkeldiagrammer og søjlediagrammer — og vi kigger på, om stikprøven er stor nok til at sige noget.</p>
<a class="btnlink ghost" href="statistik.html">Genopfrisk statistik</a></div>
</main>
<footer>Undervisningsmateriale · 9. klasse · Mibelibsen.</footer>'''
    dok = (f'<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>Ung i Tyskland · Tysk · 9. klasse</title>'
           f'<style>{CSS_SIDE}</style></head><body>{krop}</body></html>')
    open(SIDE, 'w', encoding='utf-8').write(dok)


# ------------------------------------------------------------------- main
def main():
    scratch = os.environ.get('SCRATCH', '/tmp/byg_spoergeskema')
    unger = laes_unger()
    n = skriv_redirects(unger)
    print(f'skrevet:  vercel.json   {n} redirects under /u/')
    skriv_side(unger)
    print(f'skrevet:  {SIDE}')
    skriv_tsv(unger)
    print(f'skrevet:  {MAPPE}/unger-links.tsv   {len(unger)} unger')
    skriv_plakater(unger, scratch)
    tjek_qr(unger)
    if not FORMULAR:
        print('BEMÆRK:   der er intet link til spørgeskemaet i opsaetning.json — '
              'koderne fører indtil videre til siden. Kør igen, når linket er sat ind.')
    if not unger:
        print('BEMÆRK:   spoergeskema/unger.txt er tom — kun eksemplet er bygget.')


if __name__ == '__main__':
    main()
