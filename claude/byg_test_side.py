# -*- coding: utf-8 -*-
"""Bygger test-statistik.html og test-statistik-resultater.html.

Quiz-motoren og formgivningen genbruges fra manipulation.html, saa der kun er
én motor i projektet. Spoergsmaalene kommer fra quiz.json, som byg_quiz.py
skriver - de fire formater kan derfor ikke sige noget forskelligt.

Afleveringskoden: siden er statisk og har ingen server, saa ungen faar en kort
kode med sit navn, sin score og 30 bit for rigtigt/forkert. Laereren indsaetter
koderne paa resultatsiden og faar en tabel. Koden indeholder ikke facit, kun om
det enkelte svar var rigtigt.

Koer:  python3 claude/byg_test_side.py <mappe-med-quiz.json>
"""
import sys, os, json, html, re

FIGDIR = sys.argv[1] if len(sys.argv) > 1 else 'quizfig'
SP = json.load(open(os.path.join(FIGDIR, 'quiz.json')))
assert len(SP) == 30

MODULER = [('Beskriv data', 1, 11,
            'Median, typetal, variationsbredde, gennemsnit og kvartiler — '
            'og hvad et boksplot egentlig viser.'),
           ('Diagrammer', 12, 16,
            'Cirkeldiagrammet i grader og procent. Husk: hele cirklen er 360°, '
            'og alle frekvenser giver 100 %.'),
           ('Sumkurve og frekvens', 17, 21,
            'Aflæsning på sumkurve, kumuleret frekvens, histogram og '
            'søjlediagram.'),
           ('Sandsynlighed', 22, 24,
            'Udfaldsrummet for to terninger. Tæl felterne — der er 36 i alt.'),
           ('Manipulation', 25, 30,
            'Procentpoint mod procent, svarprocent, afskåret akse og '
            'arealtricket.')]
assert sum(b - a + 1 for _, a, b, _ in MODULER) == len(SP)

kilde = open('manipulation.html').read()
CSS = re.findall(r'(?s)<style>(.*?)</style>', kilde)[-1]
MOTOR = re.findall(r'(?s)<script>(.*?)</script>', kilde)[-1]

EKSTRA_CSS = """
  .qfig{background:var(--panel2);border:1px solid var(--line);border-radius:12px;
        padding:10px 12px;margin:10px 0 12px;text-align:center}
  .qfig svg{max-width:100%;height:auto}
  .kodeboks{background:var(--accent-soft);border:1px solid var(--accent);
            border-radius:14px;padding:18px 20px;margin:18px 0}
  .kodeboks h3{margin:0 0 6px;font-size:1.1rem}
  .kodeboks p{margin:6px 0;color:var(--muted);font-size:.95rem}
  .kode{font-family:Consolas,"Courier New",monospace;font-size:1.25rem;
        font-weight:700;letter-spacing:1px;background:#fff;border:1px solid var(--line);
        border-radius:10px;padding:12px 16px;margin:10px 0;word-break:break-all;
        color:#111}
  .kodeboks .btn{margin-right:8px}
  textarea.koder{width:100%;min-height:180px;font-family:Consolas,monospace;
        font-size:.95rem;border:1px solid var(--line);border-radius:10px;padding:12px}
  table.rtable td.smal{white-space:nowrap}
  .fejlliste{color:var(--bad);font-size:.9rem}
"""


def attr(tekst):
    """Escaper kun det, en dobbeltcitationsafgraenset attribut ikke taaler.

    Forklaringerne indeholder markup til broeker og saettes med innerHTML, saa
    < og > skal staa uroerte. Broekerne bruger enkeltcitationstegn netop derfor.
    """
    return tekst.replace('&', '&amp;').replace('"', '&quot;')

# --------------------------------------------------------------- spørgsmål
BOGSTAV = 'ABCD'


def q_html(s, nr_i_modul):
    opts = ''.join(
        f'<button class="opt"><span class="mk">{BOGSTAV[j]}</span> '
        f'{html.escape(sv)}</button>' for j, sv in enumerate(s['sv']))
    return (f'<div class="q" data-answer="{s["rigtig"]}" '
            f'data-exp="{attr(s["forklaring"])}">'
            f'<div class="qtext"><span class="qn">{nr_i_modul}.</span> '
            f'{html.escape(s["q"])}</div>'
            f'<div class="qfig">{s["svg"]}</div>'
            f'<div class="opts">{opts}</div><div class="fb"></div></div>')


sektioner = []
for i, (navn, fra, til, tekst) in enumerate(MODULER, 1):
    sp = [s for s in SP if fra <= s['nr'] <= til]
    qs = ''.join(q_html(s, j) for j, s in enumerate(sp, 1))
    sidst = i == len(MODULER)
    id_sidst = ' id="finalMsg"' if sidst else ''
    tekst_sidst = '' if sidst else 'Videre til næste del.'
    sektioner.append(
        f'<section class="quiz" id="modul{i}" data-quiz>'
        f'<div class="qhead"><span class="qtag">Del {i} af {len(MODULER)}</span>'
        f'<h3>{html.escape(navn)}</h3></div>'
        f'<p class="qsub">{html.escape(tekst)} Du får svar og forklaring med '
        f'det samme.</p>{qs}'
        f'<div class="scorebar"><span class="badge" data-score>0 / {len(sp)} '
        f'rigtige</span> <span{id_sidst}>{tekst_sidst}</span></div></section>')

nav = ''.join(f'<a href="#modul{i}">{html.escape(n)}</a>'
              for i, (n, _, _, _) in enumerate(MODULER, 1))

KODE_JS = """
(function(){
  // Siden er statisk. Derfor faar ungen en kode med navn, score og 30 bit for
  // rigtigt/forkert, som laereren saetter ind paa resultatsiden. Koden
  // indeholder ikke facit - kun om svaret var rigtigt.
  var ALFABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';   // uden I, L, O og U
  var KEY = document.body.getAttribute('data-store-key');
  var qs = Array.prototype.slice.call(document.querySelectorAll('.q'));

  function tilstand(){
    try{ return JSON.parse(localStorage.getItem(KEY)) || {}; }catch(e){ return {}; }
  }
  function base32(n, cifre){
    var s = '';
    for(var i = 0; i < cifre; i++){ s = ALFABET[n % 32] + s; n = Math.floor(n / 32); }
    return s;
  }
  function lavKode(){
    var st = tilstand(), valgt = st.chosen || {}, ubesvaret = [];
    var bits = 0, rigtige = 0;
    qs.forEach(function(q, i){
      var facit = parseInt(q.getAttribute('data-answer'), 10);
      if(!(i in valgt)){ ubesvaret.push(i + 1); return; }
      if(valgt[i] === facit){ rigtige++; bits += Math.pow(2, i); }
    });
    return {navn: (st.name || '').trim(), rigtige: rigtige, bits: bits,
            ubesvaret: ubesvaret};
  }
  function tegn(){
    var r = lavKode();
    var boks = document.getElementById('kodeUd');
    var fejl = document.getElementById('kodeFejl');
    if(r.ubesvaret.length){
      boks.textContent = '—';
      fejl.textContent = 'Du mangler at svare på ' + r.ubesvaret.length +
        ' spørgsmål: nummer ' + r.ubesvaret.join(', ') + '.';
      return;
    }
    if(!r.navn){
      boks.textContent = '—';
      fejl.textContent = 'Skriv dit navn øverst på siden først (knappen "Skift bruger").';
      return;
    }
    fejl.textContent = '';
    // 30 bit deles i to halvdele, saa tallet holder sig praecist
    var lav = r.bits % 32768, hoej = Math.floor(r.bits / 32768);
    var krop = base32(hoej, 3) + base32(lav, 3);
    var sum = 0;
    for(var i = 0; i < krop.length; i++) sum += ALFABET.indexOf(krop[i]);
    boks.textContent = r.navn.toUpperCase().replace(/[^A-ZÆØÅ]/g, '') + '-' +
      r.rigtige + '-' + krop + ALFABET[(sum + r.rigtige) % 32];
  }
  document.getElementById('kodeBtn').addEventListener('click', tegn);
  document.getElementById('kopiBtn').addEventListener('click', function(){
    var t = document.getElementById('kodeUd').textContent;
    if(t && t !== '—'){
      navigator.clipboard.writeText(t);
      document.getElementById('kodeFejl').textContent = 'Koden er kopieret. Sæt den ind i Teams.';
    }
  });
})();
"""

SIDE = f'''<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Test · Statistik · 9. klasse</title><style>{CSS}{EKSTRA_CSS}</style></head>
<body data-store-key="test9_statistik_v1" data-modules="{'|'.join(n for n, _, _, _ in MODULER)}">
<div class="overlay" id="startOverlay"><div class="card">
<h2 id="ovTitle">Velkommen</h2>
<p id="ovText">Skriv det navn, din lærer skal kunne kende dig på. Dine svar gemmes i denne browser, så du kan fortsætte, hvor du slap.</p>
<input id="nameInput" type="text" placeholder="Dit navn" autocomplete="off" maxlength="30">
<div class="btnrow"><button class="btn" id="startBtn">Start</button>
<button class="btn ghost" id="skipBtn">Fortsæt uden navn</button></div></div></div>
<header class="top"><div class="top-inner">
<div class="brand">Matematik · <span>Test i statistik</span></div>
<nav class="jump">{nav}<a href="#results">Resultater</a>
<a class="side" href="index.html">Forside</a>
<a class="side" href="matematik.html">Matematik</a>
<a class="side" href="statistik.html">Statistik</a></nav></div></header>
<main>
<section class="hero" id="intro"><span class="pill">9. klasse · test</span>
<h1>Test i statistik</h1>
<p>30 spørgsmål med figurer. Du får svar og forklaring med det samme, og til
sidst laver du en kode, du sender til din lærer. Skriv dit navn, så gemmes dine
svar i browseren — du kan holde pause undervejs.</p>
<button class="printbtn" onclick="window.print()">Print siden</button>
<div class="welcome" id="welcomeBar"><span class="hi" id="welcomeHi"></span>
<span class="live" id="welcomeLive"></span><span class="spacer"></span>
<button class="btn ghost" id="resetBtn">Nulstil mine svar</button>
<button class="btn ghost" id="switchBtn">Skift bruger</button></div>
<div class="progress-wrap"><div class="progress-bar">
<div class="progress-fill" id="progressFill"></div></div>
<div class="progress-label" id="progressLabel">Quiz-fremgang: 0 af 30 spørgsmål besvaret</div>
</div></section>
{''.join(sektioner)}
<section class="lesson" id="results"><h2><span class="num">R</span> Dine resultater</h2>
<p class="sub" id="resultsSub">Tabellen udfyldes, efterhånden som du svarer.</p>
<table class="rtable"><thead><tr><th>Del</th><th>Rigtige</th><th>Besvaret</th></tr></thead>
<tbody id="resultsBody"></tbody></table>
<div class="grade" id="gradeMsg"></div>
<div class="kodeboks"><h3>Aflever dit resultat</h3>
<p>Når du har svaret på alle 30, laver du din kode her og sender den til din
lærer i Teams. Koden indeholder dit navn, hvor mange du havde rigtige, og
hvilke numre du missede — ikke svarene.</p>
<div class="kode" id="kodeUd">—</div>
<button class="btn" id="kodeBtn">Lav min kode</button>
<button class="btn ghost" id="kopiBtn">Kopiér</button>
<p class="fejlliste" id="kodeFejl"></p></div>
<div style="margin-top:16px"><button class="printbtn" onclick="window.print()">Print siden</button></div>
</section></main>
<footer>Undervisningsmateriale til matematik i 9. klasse · Test i statistik.</footer>
<script>{MOTOR}</script>
<script>{KODE_JS}</script>
</body></html>'''
open('test-statistik.html', 'w').write(SIDE)

# ------------------------------------------------------- lærerens resultatside
LAERER_JS = """
(function(){
  var ALFABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
  var ANTAL = 30;
  function tal(s){ var n = 0; for(var i=0;i<s.length;i++) n = n*32 + ALFABET.indexOf(s[i]); return n; }
  function laes(linje){
    var m = linje.trim().toUpperCase().match(/^([A-ZÆØÅ]+)-(\\d+)-([0-9A-Z]{6})([0-9A-Z])$/);
    if(!m) return null;
    var krop = m[3], rigtige = parseInt(m[2],10), sum = 0;
    for(var i=0;i<krop.length;i++){
      if(ALFABET.indexOf(krop[i]) < 0) return null;
      sum += ALFABET.indexOf(krop[i]);
    }
    if(ALFABET[(sum + rigtige) % 32] !== m[4]) return null;   // tjekciffer
    var bits = tal(krop.slice(0,3)) * 32768 + tal(krop.slice(3));
    var forkerte = [];
    for(var i=0;i<ANTAL;i++) if(!(Math.floor(bits / Math.pow(2,i)) % 2)) forkerte.push(i+1);
    if(ANTAL - forkerte.length !== rigtige) return null;      // score skal passe
    return {navn:m[1], rigtige:rigtige, forkerte:forkerte};
  }
  document.getElementById('afkod').addEventListener('click', function(){
    var linjer = document.getElementById('koder').value.split('\\n').filter(function(l){ return l.trim(); });
    var ok = [], daarlige = [];
    linjer.forEach(function(l){ var r = laes(l); if(r) ok.push(r); else daarlige.push(l.trim()); });
    var tb = document.getElementById('elevBody'); tb.innerHTML = '';
    ok.sort(function(a,b){ return b.rigtige - a.rigtige; }).forEach(function(r){
      var tr = document.createElement('tr');
      tr.innerHTML = '<td>' + r.navn + '</td><td class="smal">' + r.rigtige + ' / ' + ANTAL +
        '</td><td class="smal">' + Math.round(r.rigtige/ANTAL*100) + ' %</td><td>' +
        (r.forkerte.length ? r.forkerte.join(', ') : '—') + '</td>';
      tb.appendChild(tr);
    });
    var fejlPr = [];
    for(var i=1;i<=ANTAL;i++){
      var n = ok.filter(function(r){ return r.forkerte.indexOf(i) >= 0; }).length;
      fejlPr.push({nr:i, fejl:n});
    }
    var sb = document.getElementById('sporgsmaalBody'); sb.innerHTML = '';
    fejlPr.sort(function(a,b){ return b.fejl - a.fejl; }).forEach(function(f){
      if(!ok.length) return;
      var pct = Math.round((ok.length - f.fejl)/ok.length*100);
      var tr = document.createElement('tr');
      tr.innerHTML = '<td class="smal">Spørgsmål ' + f.nr + '</td><td class="smal">' +
        (ok.length - f.fejl) + ' / ' + ok.length + '</td><td class="smal">' + pct + ' % rigtige</td>';
      sb.appendChild(tr);
    });
    document.getElementById('opsummering').textContent = ok.length
      ? ok.length + ' koder aflæst. Gennemsnit: ' +
        (Math.round(ok.reduce(function(a,r){ return a + r.rigtige; },0)/ok.length*10)/10) +
        ' af ' + ANTAL + ' rigtige.'
      : 'Ingen gyldige koder endnu.';
    document.getElementById('daarlige').textContent = daarlige.length
      ? 'Kunne ikke læses (tjek for tastefejl): ' + daarlige.join(' · ') : '';
  });
})();
"""

LAERER = f'''<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Resultater · Test i statistik</title><style>{CSS}{EKSTRA_CSS}</style></head>
<body data-store-key="test9_laerer_v1">
<header class="top"><div class="top-inner">
<div class="brand">Matematik · <span>Resultater</span></div>
<nav class="jump"><a class="side" href="test-statistik.html">Testen</a>
<a class="side" href="matematik.html">Matematik</a></nav></div></header>
<main><section class="hero"><span class="pill">Til læreren</span>
<h1>Aflæs elevernes koder</h1>
<p>Sæt koderne ind — én pr. linje — og tryk på knappen. Siden regner ud, hvem
der har hvad, og hvilke spørgsmål der drillede flest. Koderne indeholder ikke
elevernes svar, kun om hvert svar var rigtigt.</p></section>
<section class="lesson"><h2><span class="num">1</span> Koderne</h2>
<textarea class="koder" id="koder" placeholder="MIA-27-K3F9T2A&#10;OLIVER-22-B7X1M4C"></textarea>
<div style="margin-top:12px"><button class="btn" id="afkod">Aflæs koderne</button></div>
<p class="sub" id="opsummering" style="margin-top:12px"></p>
<p class="fejlliste" id="daarlige"></p></section>
<section class="lesson"><h2><span class="num">2</span> Eleverne</h2>
<table class="rtable"><thead><tr><th>Navn</th><th>Rigtige</th><th>Procent</th>
<th>Missede spørgsmål</th></tr></thead><tbody id="elevBody"></tbody></table></section>
<section class="lesson"><h2><span class="num">3</span> Spørgsmålene</h2>
<p class="sub">Sorteret efter hvor mange der svarede forkert. Brug den til at se,
hvad klassen skal have igen.</p>
<table class="rtable"><thead><tr><th>Spørgsmål</th><th>Rigtige</th><th>Andel</th>
</tr></thead><tbody id="sporgsmaalBody"></tbody></table>
<svg viewBox="0 0 100 8" width="100%" style="max-width:320px;margin-top:14px"
 xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="100" height="8"
 rx="4" fill="#eaf2fd"/><rect x="0" y="0" width="62" height="8" rx="4" fill="#1f6fd6"/>
</svg><p class="sub" style="font-size:.85rem">Farvet felt = andel rigtige. Vises
her som eksempel.</p></section>
</main>
<footer>Undervisningsmateriale til matematik i 9. klasse · Resultatoversigt.</footer>
<script>{LAERER_JS}</script></body></html>'''
open('test-statistik-resultater.html', 'w').write(LAERER)
print(f'skrevet:  test-statistik.html            {len(SIDE)//1024} kb · '
      f'{len(SP)} spørgsmål i {len(MODULER)} dele')
print(f'skrevet:  test-statistik-resultater.html {len(LAERER)//1024} kb')
