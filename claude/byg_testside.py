# -*- coding: utf-8 -*-
"""Bygger afleveringssiden til samfundsfagstesten.

Forskellen paa denne side og oevelsessiden i kommende/ er den vigtigste
i hele opgaven: **her staar facit ikke i kildekoden.** Der er ingen
data-answer, ingen feedback og ingen point undervejs. Siden samler svar
og sender dem til Supabase; rettelsen sker bagefter mod en facittabel,
som sidens offentlige noegle hverken kan laese eller skrive i.

Adressen er ikke til at gaette og linkes ikke fra nogen side. Den staar
dog i det offentlige repo — den, der leder i GitHub, kan finde den.
Kodeordet er derfor ogsaa et krav i databasens insert-politik, saa en
tilfaeldig forbipasserende ikke kan fylde tabellen.

    python3 claude/byg_testside.py
"""
import html
import importlib.util
import json
import os
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)

_spec = importlib.util.spec_from_file_location(
    'testen', os.path.join(HER, 'byg_samfundsfagstest.py'))
T = importlib.util.module_from_spec(_spec)
sys.modules['testen'] = T
_spec.loader.exec_module(T)

_fspec = importlib.util.spec_from_file_location(
    'pakken', os.path.join(HER, 'byg_forms_pakke.py'))
P = importlib.util.module_from_spec(_fspec)
sys.modules['pakken'] = P
_fspec.loader.exec_module(P)

FILNAVN = 't/samf-81e7bc5fe466.html'
UD = os.path.join(ROD, FILNAVN)
PROEVE = 'samfundsfag-60'
KODE = 'kontiki26'
SUPABASE = 'https://pxdnszdukyjnbfmcpbvi.supabase.co'
# Publicerbar noegle. Den er lavet til at staa i klientkode: den kan kun
# det, raekkesikkerheden tillader, og her er det én ting — indsaette en
# besvarelse. Den kan ikke laese besvarelser og ikke se facit.
NOEGLE = 'sb_publishable_PvPfK3dFW7I2A0U-31Z5Qw_-uIOnzPe'

CSS = '''
:root{--ink:#1a2233;--muted:#586074;--line:#c9d2e0;--panel:#f3f6fb;
--accent:#1f6fd6;--ok:#1a8f5e;--bg:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-size:17px;
line-height:1.5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',
Roboto,Helvetica,Arial,sans-serif;padding-bottom:92px}
main{max-width:760px;margin:0 auto;padding:0 16px}
header.top{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.95);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-inner{max-width:760px;margin:0 auto;padding:11px 16px;display:flex;
align-items:baseline;gap:10px;flex-wrap:wrap}
.brand{font-weight:800}.brand span{color:var(--accent)}
.hero{padding:26px 0 8px}
.hero h1{font-size:1.75rem;margin:6px 0 10px}
.pill{display:inline-block;background:var(--panel);border:1px solid var(--line);
border-radius:999px;padding:3px 11px;font-size:.78rem;color:var(--muted);
letter-spacing:.04em;text-transform:uppercase;font-weight:700}
.hero p{color:var(--muted);max-width:62ch}
.kort{border:1px solid var(--line);border-radius:14px;padding:18px 20px;
margin:18px 0;background:#fff}
.kort h2{font-size:1.1rem;margin:0 0 10px}
label{display:block;font-weight:700;font-size:.9rem;margin:12px 0 4px}
input[type=text]{width:100%;max-width:340px;font-size:1.05rem;padding:11px 13px;
border:1.5px solid var(--line);border-radius:10px;font-family:inherit}
input[type=text]:focus{outline:none;border-color:var(--accent)}
.hint{color:var(--muted);font-size:.88rem;margin:4px 0 0}
.q{border-top:1px solid var(--line);padding:22px 0 6px}
.q:first-of-type{border-top:0}
.qtext{font-weight:600;margin-bottom:4px;display:flex;gap:10px}
.qn{color:var(--accent);font-weight:800;flex:0 0 auto}
.qfig{margin:12px 0}
.qfig svg{width:100%;max-width:520px;height:auto;display:block;margin:0 auto}
.opt{display:flex;align-items:center;gap:12px;width:100%;text-align:left;
background:#fff;border:1.5px solid var(--line);border-radius:12px;
padding:13px 15px;margin:8px 0;font:inherit;color:inherit;cursor:pointer}
.opt:hover{border-color:var(--accent);background:var(--panel)}
.opt .mk{flex:0 0 auto;width:28px;height:28px;border-radius:8px;display:grid;
place-items:center;background:var(--panel);border:1px solid var(--line);
font-weight:800;font-size:.85rem}
.opt[aria-pressed=true]{border-color:var(--accent);background:#eaf2fd}
.opt[aria-pressed=true] .mk{background:var(--accent);color:#fff;
border-color:var(--accent)}
.bund{position:fixed;left:0;right:0;bottom:0;z-index:40;background:#fff;
border-top:1px solid var(--line);box-shadow:0 -4px 16px rgba(26,34,51,.07)}
.bund-inner{max-width:760px;margin:0 auto;padding:11px 16px;display:flex;
align-items:center;gap:14px;flex-wrap:wrap}
.bar{flex:1 1 180px;height:9px;border-radius:999px;background:var(--panel);
overflow:hidden;min-width:120px}
.bar i{display:block;height:100%;width:0;background:var(--accent);
transition:width .25s}
.taeller{font-size:.9rem;color:var(--muted);font-variant-numeric:tabular-nums}
button.send{background:var(--accent);color:#fff;border:0;border-radius:10px;
padding:11px 20px;font:inherit;font-weight:700;cursor:pointer}
button.send:disabled{background:var(--line);cursor:not-allowed}
.besked{padding:10px 14px;border-radius:10px;margin:12px 0;font-size:.95rem}
.besked.fejl{background:#fdeaec;border:1px solid #c23b4b;color:#8b1a2b}
.besked.ok{background:#e6f5ee;border:1px solid var(--ok);color:#13593d}
#kvittering{display:none;text-align:center;padding:60px 20px}
#kvittering h2{font-size:1.5rem}
#kvittering .flueben{width:66px;height:66px;border-radius:50%;
background:var(--ok);color:#fff;display:grid;place-items:center;
font-size:2rem;margin:0 auto 18px}
footer{color:var(--muted);font-size:.86rem;text-align:center;
padding:30px 16px 20px;border-top:1px solid var(--line);margin-top:30px}
@media(max-width:600px){body{font-size:16px}.hero h1{font-size:1.45rem}}
'''


# figurnummer -> den faerdige SVG. P.figurer har parrene i forvejen.
FIGUR = {nr: svg for nr, svg, _ in P.figurer}


def spm_html():
    ud = []
    for nr, fignr, tekst, valg, _plads, _forkl, _del in P.SPM:
        knapper = ''.join(
            f'<button class="opt" type="button" aria-pressed="false" '
            f'data-q="{nr}" data-v="{i}"><span class="mk">{"ABC"[i]}</span>'
            f'<span>{html.escape(v)}</span></button>'
            for i, v in enumerate(valg))
        ud.append(
            f'<section class="q" id="q{nr}"><div class="qtext">'
            f'<span class="qn">{nr}.</span><span>{html.escape(tekst)}</span>'
            f'</div><div class="qfig">{FIGUR[fignr]}</div>'
            f'<div class="opts">{knapper}</div></section>')
    return ''.join(ud)


JS = '''
(function(){
  var ANTAL=%(antal)d, PROEVE=%(proeve)s, KODE=%(kode)s;
  var URL=%(url)s+'/rest/v1/skole_test_svar', NOEGLE=%(noegle)s;
  var GEM='samf60_kladde_v1';
  var svar=new Array(ANTAL).fill(-1), start=Date.now(), sendt=false;

  // Kladden ligger i browseren, saa et tabt net eller en lukket fane
  // ikke koster en halv time. Den er kun paa denne maskine.
  try{var g=JSON.parse(localStorage.getItem(GEM)||'null');
    if(g&&g.svar&&g.svar.length===ANTAL){svar=g.svar;
      if(g.navn)document.getElementById('navn').value=g.navn;
      if(g.klasse)document.getElementById('klasse').value=g.klasse;}
  }catch(e){}

  function gem(){try{localStorage.setItem(GEM,JSON.stringify({svar:svar,
    navn:document.getElementById('navn').value,
    klasse:document.getElementById('klasse').value}));}catch(e){}}

  function tegn(){
    document.querySelectorAll('.opt').forEach(function(b){
      b.setAttribute('aria-pressed', svar[+b.dataset.q-1]===+b.dataset.v?'true':'false');
    });
    var n=svar.filter(function(v){return v>=0;}).length;
    document.getElementById('taeller').textContent=n+' af '+ANTAL+' besvaret';
    document.querySelector('.bar i').style.width=(n/ANTAL*100)+'%%';
  }

  document.addEventListener('click',function(e){
    var b=e.target.closest('.opt'); if(!b||sendt)return;
    svar[+b.dataset.q-1]=+b.dataset.v; gem(); tegn();
  });
  ['navn','klasse'].forEach(function(id){
    document.getElementById(id).addEventListener('input',gem);
  });

  function vis(txt,slags){
    var d=document.getElementById('besked');
    d.className='besked '+slags; d.textContent=txt; d.style.display='block';
  }

  document.getElementById('send').addEventListener('click',function(){
    if(sendt)return;
    var navn=document.getElementById('navn').value.trim();
    var klasse=document.getElementById('klasse').value.trim();
    if(!navn){vis('Skriv dit fornavn øverst, før du afleverer.','fejl');
      document.getElementById('navn').focus();window.scrollTo(0,0);return;}
    if(!klasse){vis('Skriv din klasse øverst, før du afleverer.','fejl');
      document.getElementById('klasse').focus();window.scrollTo(0,0);return;}
    var mangler=svar.filter(function(v){return v<0;}).length;
    if(mangler&&!confirm('Du mangler '+mangler+' spørgsmål. Vil du aflevere alligevel?'))return;

    var knap=document.getElementById('send');
    knap.disabled=true; knap.textContent='Sender…';
    fetch(URL,{method:'POST',headers:{'apikey':NOEGLE,
      'Authorization':'Bearer '+NOEGLE,'Content-Type':'application/json',
      'Prefer':'return=minimal'},
      body:JSON.stringify({proeve:PROEVE,kode:KODE,navn:navn,klasse:klasse,
        svar:svar,sekunder:Math.round((Date.now()-start)/1000)})})
    .then(function(r){
      if(!r.ok)throw new Error('HTTP '+r.status);
      sendt=true;
      try{localStorage.removeItem(GEM);}catch(e){}
      document.getElementById('testen').style.display='none';
      document.querySelector('.bund').style.display='none';
      var k=document.getElementById('kvittering');
      k.style.display='block';
      document.getElementById('kvitnavn').textContent=navn;
      window.scrollTo(0,0);
    })
    .catch(function(err){
      knap.disabled=false; knap.textContent='Aflever';
      vis('Det kunne ikke sendes ('+err.message+'). Dine svar er gemt i '+
        'browseren — prøv igen om et øjeblik, og sig til læreren, hvis '+
        'det bliver ved.','fejl');
    });
  });

  window.addEventListener('beforeunload',function(e){
    if(!sendt&&svar.some(function(v){return v>=0;})){e.preventDefault();e.returnValue='';}
  });
  tegn();
})();
'''


def byg():
    js = JS % dict(antal=len(P.SPM), proeve=json.dumps(PROEVE),
                   kode=json.dumps(KODE), url=json.dumps(SUPABASE),
                   noegle=json.dumps(NOEGLE))
    return ('<!DOCTYPE html><html lang="da"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex,nofollow">'
            '<title>Samfundsfagstest · 9. klasse</title>'
            f'<style>{CSS}</style></head><body>'
            '<header class="top"><div class="top-inner">'
            '<span class="brand">321flyv · <span>Samfundsfagstest</span></span>'
            '</div></header>'
            '<main><div id="testen">'
            '<section class="hero"><span class="pill">9. klasse · samfundsfag</span>'
            f'<h1>Samfundsfagstest</h1><p>{len(P.SPM)} spørgsmål. '
            'Du får <b>ikke</b> at vide undervejs, om du svarer rigtigt — '
            'det er en test, ikke en øvelse. Du kan gå frem og tilbage og '
            'rette, så længe du ikke har afleveret. Svarene gemmes i '
            'browseren undervejs, så du ikke mister dem.</p></section>'
            '<div class="kort"><h2>Hvem er du?</h2>'
            '<label for="navn">Fornavn</label>'
            '<input type="text" id="navn" autocomplete="off" '
            'placeholder="fx Sofie" maxlength="30">'
            '<label for="klasse">Klasse</label>'
            '<input type="text" id="klasse" autocomplete="off" '
            'placeholder="fx 9. klasse" maxlength="10">'
            '<p class="hint">Kun fornavn og klasse. Din lærer skal kunne se, '
            'hvem der har afleveret.</p>'
            '<div id="besked" class="besked" style="display:none"></div></div>'
            + spm_html() +
            '</div>'
            '<section id="kvittering"><div class="flueben">&#10003;</div>'
            '<h2>Afleveret</h2><p>Tak, <b id="kvitnavn"></b>. '
            'Din besvarelse er sendt til din lærer. Du kan lukke siden nu.</p>'
            '</section></main>'
            '<div class="bund"><div class="bund-inner">'
            '<span class="taeller" id="taeller">0 af 60 besvaret</span>'
            '<span class="bar"><i></i></span>'
            '<button class="send" id="send" type="button">Aflever</button>'
            '</div></div>'
            '<footer>Samfundsfag · 9. klasse. Kun fornavn og klasse gemmes.'
            '</footer>'
            f'<script>{js}</script></body></html>')


if __name__ == '__main__':
    os.makedirs(os.path.dirname(UD), exist_ok=True)
    doc = byg()
    assert 'data-answer' not in doc, 'facit må ikke stå i siden'
    assert 'data-exp' not in doc, 'forklaringerne må ikke stå i siden'
    for _, _, _, _, plads, forkl, _ in P.SPM:
        assert forkl not in doc
    assert doc.count('class="q"') == len(P.SPM)
    open(UD, 'w', encoding='utf-8').write(doc)
    print(f'skrevet:  {FILNAVN}  ·  {len(P.SPM)} spørgsmål, '
          f'{doc.count("<svg")} figurer, {len(doc)//1024} kB')
    print(f'          ingen facit i kildekoden: kontrolleret')
