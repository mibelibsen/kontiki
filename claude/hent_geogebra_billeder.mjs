// Henter skaermbillederne til Intro til GeoGebra fra den rigtige app.
//
// Billederne maa ikke tegnes i haanden: saa holder de op med at ligne det,
// ungen ser. Scriptet aabner geogebra.org/classic i Chromium paa dansk,
// bygger hver tilstand med appens eget API og fotograferer vinduet.
//
//     node claude/hent_geogebra_billeder.mjs
//     python3 claude/beskaer_geogebra_billeder.py
//
// Kommandonavnene i ggbApplet.evalCommand er de ENGELSKE - API'et er ikke
// oversat - men algebravinduet viser de danske (Linje, Haeldning), og det
// er dem, der kommer med paa billedet.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';

const UD = new URL('../billeder/geogebra/', import.meta.url).pathname;
const b = await chromium.launch();
const ctx = await b.newContext({
  locale: 'da-DK', viewport: { width: 1200, height: 700 }, deviceScaleFactor: 2,
});
const p = await ctx.newPage();
await p.goto('https://www.geogebra.org/classic?lang=da',
             { waitUntil: 'networkidle', timeout: 90000 });
await p.waitForTimeout(7000);

// 1 — app-listen, som den kommer frem ved foerste besoeg
const pop = await p.$('.perspectivePopup');
if (!pop) throw new Error('app-listen kom ikke frem — er forsiden lavet om?');
await pop.screenshot({ path: `${UD}1-vaelg-graf.png` });

await p.mouse.click(700, 400);
await p.waitForTimeout(1200);
await p.addStyleTag({ content: '.KeyBoard{display:none!important}' });

const ggb = async (...c) => {
  await p.evaluate(k => k.forEach(x => window.ggbApplet.evalCommand(x)), c);
  await p.waitForTimeout(1200);
};
const zoom = async (x1, y1, x2, y2) => {
  await p.evaluate(v => window.ggbApplet.setCoordSystem(...v), [x1, x2, y1, y2]);
  await p.waitForTimeout(800);
};

await p.screenshot({ path: `${UD}2-vinduet.png` });
await ggb('A=(1,3)', 'B=(4,9)');
await zoom(-1, -1, 6, 11);
await p.screenshot({ path: `${UD}3-punkter.png` });

await ggb('f=Line(A,B)');
await p.screenshot({ path: `${UD}4-linje.png` });
await (await p.$('.algebraPanel')).screenshot({ path: `${UD}4b-ligningen.png` });

await ggb('a=Slope(f)');
await p.screenshot({ path: `${UD}5-haeldning.png` });
await ggb('g(x)=2x+1');
await p.screenshot({ path: `${UD}6-egen-forskrift.png` });
await ggb('Root(g)');
await zoom(-3, -2, 6, 11);
await p.screenshot({ path: `${UD}7-rod.png` });
await ggb('h(x)=x+4', 'S=Intersect(g,h)');
await p.screenshot({ path: `${UD}8-skaering.png` });

// vaerdien g(7) paa en ren tavle
const p2 = await ctx.newPage();
await p2.goto('https://www.geogebra.org/classic?lang=da',
              { waitUntil: 'networkidle', timeout: 90000 });
await p2.waitForTimeout(7000);
await p2.mouse.click(700, 400);
await p2.waitForTimeout(1200);
await p2.addStyleTag({ content: '.KeyBoard{display:none!important}' });
await p2.evaluate(() => {
  ['A=(1,3)', 'B=(4,9)', 'f=Line(A,B)', 'g(x)=2x+1', 'v=g(7)']
    .forEach(c => window.ggbApplet.evalCommand(c));
  window.ggbApplet.setCoordSystem(-1, 8, -1, 16);
});
await p2.waitForTimeout(2000);
const v = await p2.evaluate(() => window.ggbApplet.getValueString('v'));
if (!/15/.test(v)) throw new Error(`g(7) gav ${v} — vejledningen siger 15`);
await p2.screenshot({ path: `${UD}11-vaerdi.png` });

// menuen med Fil -> Eksporter billede
const p3 = await ctx.newPage();
await p3.goto('https://www.geogebra.org/classic?lang=da',
              { waitUntil: 'networkidle', timeout: 90000 });
await p3.waitForTimeout(7000);
await p3.mouse.click(700, 400);
await p3.waitForTimeout(1200);
await p3.addStyleTag({ content: '.KeyBoard{display:none!important}' });
await p3.evaluate(() => {
  ['A=(1,3)', 'B=(4,9)', 'f=Line(A,B)'].forEach(c => window.ggbApplet.evalCommand(c));
  window.ggbApplet.setCoordSystem(-1, 6, -1, 11);
});
await p3.waitForTimeout(1500);
const h = await p3.$('[aria-label="Hovedmenu"], [aria-label*="enu"], .mainMenuBtn');
if (h) await h.click(); else await p3.mouse.click(1168, 26);
await p3.waitForTimeout(1500);
const fil = await p3.$('text=Fil');
if (fil) { await fil.click(); await p3.waitForTimeout(1500); }
await p3.screenshot({ path: `${UD}10-menu.png` });

console.log('hentet: 11 raa skærmbilleder i billeder/geogebra/');
console.log('kør nu: python3 claude/beskaer_geogebra_billeder.py');
await b.close();
