# -*- coding: utf-8 -*-
"""Bygger laererens resultatside til samfundsfagstesten.

Siden viser afleveringerne live: den henter dem gennem de to
SECURITY DEFINER-funktioner i Supabase, som kraever laererkoden. Koden
staar **ikke** i kildekoden — den skrives ind i feltet og gemmes kun i
browserens localStorage paa den telefon eller computer, der bruger den.

Facit staar heller ikke i kildekoden. Siden viser hvor mange der svarede
rigtigt paa hvert spoergsmaal, men aldrig hvad det rigtige svar var.
Spoergsmaalsteksterne staar der, og de staar i forvejen paa selve
testsiden, saa de roeber ingenting nyt.

Soejlerne er én farve, fordi de maaler én ting (procent rigtige). Tallet
staar ved siden af hver soejle, saa farven aldrig er den eneste
oplysning.

    python3 claude/byg_resultatside.py
"""
import html
import importlib.util
import json
import os
import re
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(HER)
sys.path.insert(0, HER)

_fspec = importlib.util.spec_from_file_location(
    'pakken', os.path.join(HER, 'byg_forms_pakke.py'))
P = importlib.util.module_from_spec(_fspec)
sys.modules['pakken'] = P
_fspec.loader.exec_module(P)

FILNAVN = 't/resultat-26ec8aa4376a.html'
UD = os.path.join(ROD, FILNAVN)
PROEVE = 'samfundsfag-60'
SUPABASE = 'https://pxdnszdukyjnbfmcpbvi.supabase.co'
# Samme publicerbare noegle som afleveringssiden. Den kan intet i sig
# selv: funktionerne bag kraever laererkoden, og uden den svarer de
# "forkert kode".
NOEGLE = 'sb_publishable_PvPfK3dFW7I2A0U-31Z5Qw_-uIOnzPe'

# [nr, spoergsmaalstekst, emne] — uden svarmuligheder og uden facit.
SPM = [[nr, tekst, delnavn]
       for (nr, _fig, tekst, _valg, _plads, _forkl, delnavn) in P.SPM]
EMNER = []
for _, _, _e in SPM:
    if _e not in EMNER:
        EMNER.append(_e)

CSS = '''
:root{--ink:#1a2233;--muted:#586074;--line:#c9d2e0;--panel:#f3f6fb;
--accent:#1f6fd6;--svag:#e3ebf7;--ok:#1a8f5e;--rod:#c23b4b;--bg:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-size:17px;
line-height:1.5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',
Roboto,Helvetica,Arial,sans-serif;padding-bottom:48px}
main{max-width:860px;margin:0 auto;padding:0 16px}
header.top{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.95);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-inner{max-width:860px;margin:0 auto;padding:11px 16px;display:flex;
align-items:center;gap:10px;flex-wrap:wrap}
.top-inner strong{font-size:17px}
.top-inner .sub{color:var(--muted);font-size:14px}
.top-inner .fyld{flex:1}
.live{display:inline-flex;align-items:center;gap:7px;font-size:13px;
color:var(--muted);white-space:nowrap}
.live i{width:9px;height:9px;border-radius:50%;background:var(--ok);
display:inline-block;flex:none}
.live.tier i{background:var(--line)}
@keyframes puls{0%,100%{opacity:1}50%{opacity:.25}}
.live.henter i{animation:puls 1s infinite}
h1{font-size:25px;margin:26px 0 8px}
h2{font-size:19px;margin:34px 0 10px}
h2 .lille{font-weight:400;color:var(--muted);font-size:15px}
p{margin:10px 0}
.panel{background:var(--panel);border:1px solid var(--line);
border-radius:12px;padding:18px;margin:26px 0}
label{display:block;font-weight:600;font-size:15px;margin:14px 0 5px}
input[type=password],input[type=text]{width:100%;max-width:320px;
font-size:17px;padding:11px 12px;border:1px solid var(--line);
border-radius:9px;background:#fff;color:var(--ink);font-family:inherit}
input:focus{outline:2px solid var(--accent);outline-offset:1px}
button{font:inherit;font-size:16px;font-weight:600;padding:11px 18px;
border:1px solid var(--accent);border-radius:9px;background:var(--accent);
color:#fff;cursor:pointer;margin-top:14px}
button.stille{background:#fff;color:var(--accent);margin-top:0}
button:hover{filter:brightness(1.07)}
.fejl{color:var(--rod);font-weight:600;min-height:1.5em;margin:10px 0 0}

.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;
margin:20px 0 6px}
.tile{border:1px solid var(--line);border-radius:12px;padding:13px 14px}
.tile .navn{font-size:13px;color:var(--muted);letter-spacing:.01em}
.tile .tal{font-size:30px;font-weight:700;line-height:1.15;
font-variant-numeric:tabular-nums}
.tile .tal em{font-size:17px;font-weight:600;font-style:normal;
color:var(--muted)}
.tile .under{font-size:13px;color:var(--muted)}

.bars{display:grid;gap:7px}
.bar{display:grid;grid-template-columns:1fr 46px;align-items:center;
gap:10px}
.bar .navn{font-size:15px}
.bar .spor{height:11px;background:var(--svag);border-radius:4px;
margin-top:3px;overflow:hidden}
.bar .fyld{height:11px;background:var(--accent);border-radius:0 4px 4px 0}
.bar .pct{text-align:right;font-variant-numeric:tabular-nums;
font-weight:600;font-size:15px}
.bar .pct small{display:block;font-weight:400;color:var(--muted);
font-size:12px}

.svoeb{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:16px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);
white-space:nowrap}
th{font-size:13px;color:var(--muted);font-weight:600;background:var(--panel);
position:sticky;top:0}
th.kl{cursor:pointer;user-select:none}
th.kl:hover{color:var(--accent)}
th .pil{opacity:0}
th.aktiv{color:var(--accent)}
th.aktiv .pil{opacity:1}
td.tal{text-align:right;font-variant-numeric:tabular-nums}
td.navn{font-weight:600}
td.tekst{white-space:normal;min-width:260px;font-size:15px}
td.spor{width:120px;min-width:120px}
td.spor div{height:10px;background:var(--svag);border-radius:4px}
td.spor div i{display:block;height:10px;background:var(--accent);
border-radius:0 4px 4px 0}
tr.lav td.navn{color:var(--rod)}
.emnechip{display:inline-block;font-size:12px;color:var(--muted);
border:1px solid var(--line);border-radius:999px;padding:1px 8px;
margin-left:6px;white-space:nowrap}
.vaerktoej{display:flex;gap:10px;flex-wrap:wrap;margin:26px 0 0}
.vaerktoej button{margin-top:0}
.tom{color:var(--muted)}
@media (max-width:640px){
  body{font-size:16px}
  .tiles{grid-template-columns:repeat(2,1fr)}
  .tile .tal{font-size:26px}
  h1{font-size:22px}
  table{font-size:15px}
  th,td{padding:7px 8px}
  .skjul,.telefonskjul{display:none}
  td.tekst{min-width:0}
  td.spor{width:64px;min-width:64px}
}
@media print{
  header.top,.vaerktoej,#laas{display:none}
  .svoeb{overflow:visible}
  th{position:static}
}
'''

JS = r'''
(function(){
  var URL=__URL__, NOEGLE=__NOEGLE__, PROEVE=__PROEVE__;
  var SPM=__SPM__, EMNER=__EMNER__, ANTAL=SPM.length;
  var GEM='samf60_laererkode_v1', TIK=20000;
  var elever=[], tal=[], kode='', timer=null, henter=false;
  var sort={felt:'procent',ned:true};

  var E=function(id){return document.getElementById(id)};
  function txt(n){return String(n)}
  function pct(v){return Math.round(v)+' %'}
  function tid(s){
    s=Math.max(0,Math.round(s||0));
    var m=Math.floor(s/60);
    return m?m+' min '+(s%60)+' s':s+' s';
  }
  function klokken(iso){
    var d=new Date(iso);
    if(isNaN(d)) return '';
    var t=function(n){return (n<10?'0':'')+n};
    return t(d.getDate())+'.'+t(d.getMonth()+1)+'. '+t(d.getHours())+':'+t(d.getMinutes());
  }
  function esc(s){
    return String(s).replace(/[&<>"]/g,function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});
  }

  function kald(navn, cb){
    fetch(URL+'/rest/v1/rpc/'+navn,{method:'POST',
      headers:{'apikey':NOEGLE,'Authorization':'Bearer '+NOEGLE,
               'Content-Type':'application/json'},
      body:JSON.stringify({kode:kode,p:PROEVE})})
    .then(function(r){
      return r.json().then(function(j){return {ok:r.ok,j:j}});
    }).then(function(s){
      if(!s.ok) return cb(s.j && s.j.message ? s.j.message : 'serverfejl');
      cb(null,s.j);
    }).catch(function(){cb('ingen forbindelse')});
  }

  function hent(stille){
    if(henter) return;
    henter=true;
    E('live').className='live henter';
    E('livetxt').textContent='henter …';
    kald('skole_test_resultater',function(f1,r1){
      if(f1){ henter=false; fejlet(f1,stille); return; }
      kald('skole_test_spoergsmaalstal',function(f2,r2){
        henter=false;
        if(f2){ fejlet(f2,stille); return; }
        elever=r1||[]; tal=r2||[];
        localStorage.setItem(GEM,kode);
        E('laas').hidden=true; E('data').hidden=false;
        E('fejl').textContent='';
        E('live').hidden=false; E('live').className='live';
        E('livetxt').textContent='opdateret '+nu();
        tegn();
        if(!timer) timer=setInterval(function(){
          if(!document.hidden) hent(true);
        },TIK);
      });
    });
  }
  function nu(){
    var d=new Date(), t=function(n){return (n<10?'0':'')+n};
    return t(d.getHours())+':'+t(d.getMinutes())+':'+t(d.getSeconds());
  }
  function fejlet(besked,stille){
    if(besked==='forkert kode'){
      localStorage.removeItem(GEM);
      if(timer){clearInterval(timer);timer=null}
      E('data').hidden=true; E('laas').hidden=false;
      E('live').hidden=true;
      E('fejl').textContent='Forkert kode.';
      E('kode').value=''; E('kode').focus();
      return;
    }
    E('live').className='live tier';
    E('livetxt').textContent='kunne ikke opdatere ('+besked+')';
    if(!stille) E('fejl').textContent='Kunne ikke hente: '+besked+'.';
  }

  function tegn(){
    var n=elever.length;
    var sum=0, bedst=0, lave=0;
    for(var i=0;i<n;i++){
      var p=+elever[i].procent;
      sum+=p; if(p>bedst) bedst=p; if(p<50) lave++;
    }
    E('t-antal').textContent=n;
    E('t-gns').innerHTML=n?Math.round(sum/n)+' <em>%</em>':'–';
    E('t-bedst').innerHTML=n?bedst+' <em>%</em>':'–';
    E('t-lave').textContent=n?lave:'–';
    E('t-lave-under').textContent=n?'af '+n:'';
    E('antaltxt').textContent=n?'· '+n+(n===1?' aflevering':' afleveringer'):'';

    // emner: summér rigtige og besvarelser pr. emne
    var emne={}, k;
    for(k=0;k<EMNER.length;k++) emne[EMNER[k]]={r:0,b:0,s:0};
    var efter={};
    for(k=0;k<SPM.length;k++) efter[SPM[k][0]]=SPM[k][2];
    for(k=0;k<tal.length;k++){
      var e=efter[tal[k].nr]; if(!e||!emne[e]) continue;
      emne[e].r+=+tal[k].rigtige; emne[e].b+=+tal[k].besvarelser;
      emne[e].s++;
    }
    var raekker=[];
    for(k=0;k<EMNER.length;k++){
      var d=emne[EMNER[k]];
      raekker.push({navn:EMNER[k],
                    p:d.b?100*d.r/d.b:0, r:d.r, b:d.b, s:d.s});
    }
    raekker.sort(function(a,b){return a.p-b.p});
    var ud='';
    for(k=0;k<raekker.length;k++){
      var x=raekker[k];
      ud+='<div class="bar"><div><div class="navn">'+esc(x.navn)+
          ' <span class="emnechip">'+x.s+' spørgsmål</span></div>'+
          '<div class="spor" title="'+x.r+' rigtige af '+x.b+' svar">'+
          '<div class="fyld" style="width:'+(x.b?x.p:0).toFixed(1)+'%"></div>'+
          '</div></div><div class="pct">'+(x.b?Math.round(x.p)+' %':'–')+
          '<small>'+x.r+'/'+x.b+'</small></div></div>';
    }
    E('emner').innerHTML=n?ud:'<p class="tom">Ingen afleveringer endnu.</p>';

    // elevtabel
    var liste=elever.slice();
    liste.sort(function(a,b){
      var f=sort.felt, x=a[f], y=b[f];
      if(f==='navn'||f==='klasse'||f==='afleveret'){
        x=String(x).toLowerCase(); y=String(y).toLowerCase();
        return x<y?-1:x>y?1:0;
      }
      return (+x)-(+y);
    });
    if(sort.ned) liste.reverse();
    ud='';
    for(k=0;k<liste.length;k++){
      var r=liste[k];
      ud+='<tr'+(r.procent<50?' class="lav"':'')+'>'+
        '<td class="navn">'+esc(r.navn)+'</td>'+
        '<td class="telefonskjul">'+esc(r.klasse||'')+'</td>'+
        '<td class="tal">'+r.rigtige+'</td>'+
        '<td class="tal skjul">'+r.forkerte+'</td>'+
        '<td class="tal skjul">'+r.ubesvarede+'</td>'+
        '<td class="spor"><div title="'+r.rigtige+' af '+ANTAL+' rigtige">'+
          '<i style="width:'+r.procent+'%"></i></div></td>'+
        '<td class="tal">'+r.procent+' %</td>'+
        '<td class="tal skjul">'+tid(r.sekunder)+'</td>'+
        '<td class="skjul">'+klokken(r.afleveret)+'</td></tr>';
    }
    E('krop').innerHTML=ud||'<tr><td colspan="9" class="tom">'+
      'Ingen afleveringer endnu. Siden opdaterer sig selv, '+
      'når ungerne afleverer.</td></tr>';
    var ths=document.querySelectorAll('#tabel th.kl');
    for(k=0;k<ths.length;k++){
      ths[k].classList.toggle('aktiv',ths[k].dataset.felt===sort.felt);
      ths[k].querySelector('.pil').textContent=sort.ned?'▾':'▴';
    }

    // spørgsmålstabel — sværeste først
    var sp=tal.slice();
    sp.sort(function(a,b){
      var d=(+a.procent_rigtige)-(+b.procent_rigtige);
      return d||(a.nr-b.nr);
    });
    ud='';
    for(k=0;k<sp.length;k++){
      var q=sp[k], meta=null;
      for(var j=0;j<SPM.length;j++) if(SPM[j][0]===q.nr){meta=SPM[j];break}
      if(!meta) continue;   // gammelt spoergsmaalsnummer, ikke i prøven mere
      var p2=Math.round(q.procent_rigtige);
      ud+='<tr'+(p2<50?' class="lav"':'')+'><td class="tal">'+q.nr+'</td>'+
        '<td class="tekst">'+esc(meta?meta[1]:'')+
        '<span class="emnechip">'+esc(meta?meta[2]:'')+'</span></td>'+
        '<td class="spor"><div title="'+q.rigtige+' af '+q.besvarelser+
          ' svarede rigtigt"><i style="width:'+p2+'%"></i></div></td>'+
        '<td class="tal">'+p2+' %</td>'+
        '<td class="tal skjul">'+q.rigtige+'/'+q.besvarelser+'</td></tr>';
    }
    E('spmkrop').innerHTML=ud||'<tr><td colspan="5" class="tom">'+
      'Ingen svar endnu.</td></tr>';
  }

  function csv(){
    var r=['navn;klasse;rigtige;forkerte;ubesvarede;procent;sekunder;afleveret'];
    for(var k=0;k<elever.length;k++){
      var e=elever[k];
      r.push([e.navn,e.klasse,e.rigtige,e.forkerte,e.ubesvarede,
              e.procent,e.sekunder,e.afleveret].join(';'));
    }
    var b=new Blob(['﻿'+r.join('\r\n')],
                   {type:'text/csv;charset=utf-8'});
    var a=document.createElement('a');
    a.href=URL_O.createObjectURL(b);
    a.download='samfundsfagstest-resultater.csv';
    document.body.appendChild(a); a.click(); a.remove();
  }
  var URL_O=window.URL||window.webkitURL;

  E('aabn').addEventListener('click',function(){
    kode=E('kode').value.trim();
    if(!kode){E('fejl').textContent='Skriv lærerkoden.';return}
    E('fejl').textContent=''; hent(false);
  });
  E('kode').addEventListener('keydown',function(e){
    if(e.key==='Enter') E('aabn').click();
  });
  E('nu').addEventListener('click',function(){hent(false)});
  E('csv').addEventListener('click',csv);
  E('glem').addEventListener('click',function(){
    localStorage.removeItem(GEM);
    if(timer){clearInterval(timer);timer=null}
    kode=''; elever=[]; tal=[];
    E('data').hidden=true; E('laas').hidden=false; E('live').hidden=true;
    E('kode').value=''; E('kode').focus();
  });
  document.addEventListener('visibilitychange',function(){
    if(!document.hidden && kode) hent(true);
  });
  var ths=document.querySelectorAll('#tabel th.kl');
  for(var k=0;k<ths.length;k++) ths[k].addEventListener('click',function(){
    var f=this.dataset.felt;
    if(sort.felt===f) sort.ned=!sort.ned;
    else {sort.felt=f; sort.ned=(f!=='navn'&&f!=='klasse');}
    tegn();
  });

  var gemt=localStorage.getItem(GEM);
  if(gemt){kode=gemt; hent(true);}
'''.rstrip() + '\n})();\n'


def side():
    rk = [
        ('navn', 'Navn', ''),
        ('klasse', 'Klasse', ' telefonskjul'),
        ('rigtige', 'Rigtige', ''),
        ('forkerte', 'Forkerte', ' skjul'),
        ('ubesvarede', 'Blanke', ' skjul'),
    ]
    th = ''.join(
        f'<th class="kl{k}" data-felt="{f}">{n} <span class="pil">▾</span></th>'
        for f, n, k in rk)
    js = (JS.replace('__URL__', json.dumps(SUPABASE))
            .replace('__NOEGLE__', json.dumps(NOEGLE))
            .replace('__PROEVE__', json.dumps(PROEVE))
            .replace('__SPM__', json.dumps(SPM, ensure_ascii=False))
            .replace('__EMNER__', json.dumps(EMNER, ensure_ascii=False)))
    return f'''<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Resultater · samfundsfagstest</title>
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="top-inner">
    <strong>Resultater</strong>
    <span class="sub">Samfundsfagstest · {len(SPM)} spørgsmål</span>
    <span class="fyld"></span>
    <span class="live" id="live" hidden><i></i><span id="livetxt">—</span></span>
  </div>
</header>

<main>

<section class="panel" id="laas">
  <h1>Resultater</h1>
  <p>Her står afleveringerne fra samfundsfagstesten. Siden opdaterer sig
  selv, mens ungerne skriver. Skriv lærerkoden for at se dem.</p>
  <label for="kode">Lærerkode</label>
  <input id="kode" type="password" autocomplete="off" spellcheck="false">
  <br><button id="aabn">Vis resultater</button>
  <p class="fejl" id="fejl"></p>
</section>

<div id="data" hidden>

  <div class="tiles">
    <div class="tile"><div class="navn">Afleveret</div>
      <div class="tal" id="t-antal">–</div>
      <div class="under">besvarelser</div></div>
    <div class="tile"><div class="navn">Gennemsnit</div>
      <div class="tal" id="t-gns">–</div>
      <div class="under">rigtige svar</div></div>
    <div class="tile"><div class="navn">Bedste</div>
      <div class="tal" id="t-bedst">–</div>
      <div class="under">rigtige svar</div></div>
    <div class="tile"><div class="navn">Under 50 %</div>
      <div class="tal" id="t-lave">–</div>
      <div class="under" id="t-lave-under"></div></div>
  </div>

  <h2>Emnerne <span class="lille">— svageste først</span></h2>
  <div class="bars" id="emner"></div>

  <h2>Ungerne <span class="lille" id="antaltxt"></span></h2>
  <div class="svoeb">
  <table id="tabel">
    <thead><tr>
      {th}
      <th></th>
      <th class="kl aktiv" data-felt="procent">Procent <span class="pil">▾</span></th>
      <th class="kl skjul" data-felt="sekunder">Tid <span class="pil">▾</span></th>
      <th class="kl skjul" data-felt="afleveret">Afleveret <span class="pil">▾</span></th>
    </tr></thead>
    <tbody id="krop"></tbody>
  </table>
  </div>

  <h2>Spørgsmålene <span class="lille">— sværeste først</span></h2>
  <div class="svoeb">
  <table>
    <thead><tr><th>Nr.</th><th>Spørgsmål</th><th></th>
      <th>Rigtige</th><th class="skjul">Antal</th></tr></thead>
    <tbody id="spmkrop"></tbody>
  </table>
  </div>

  <p class="vaerktoej">
    <button id="nu" class="stille">Opdatér nu</button>
    <button id="csv" class="stille">Hent som CSV</button>
    <button id="glem" class="stille">Glem koden</button>
  </p>
</div>

</main>
<script>{js}</script>
</body>
</html>
'''


def main():
    doc = side()
    # Facit maa ikke kunne laeses ud af siden.
    uden_js = re.sub(r'(?s)<script.*?</script>', '', doc)
    for ord_ in ('data-answer', 'data-exp', 'rigtigt', 'facit'):
        assert ord_ not in uden_js.lower(), f'{ord_} staar i siden'
    assert 'kontiki26' not in doc, 'afleveringskoden skal ikke staa her'
    for nr, tekst, emne in SPM:
        assert html.escape(tekst) in doc or tekst in json.dumps(
            SPM, ensure_ascii=False), f'spoergsmaal {nr} mangler'
    os.makedirs(os.path.dirname(UD), exist_ok=True)
    with open(UD, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'skrevet:  {FILNAVN}  ·  {len(SPM)} spørgsmål, '
          f'{len(EMNER)} emner, {len(doc)//1024} kB')
    print('laererkode:  skrives ind paa siden, staar ikke i filen')


if __name__ == '__main__':
    main()
