// Skaerer de enkelte figurer ud af figurbilaget som PNG, saa de kan lægges
// ind i et Forms-spoergsmaal ét ad gangen. Figurbilaget er allerede bygget
// af byg_forms_pakke.py, saa nummereringen er den samme de to steder.
//
//   node claude/hent_testfigurer.mjs <figurbilag.html> <udmappe>
//
// Hvert billede skaleres 2x, saa det ogsaa er skarpt paa en projektor.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { pathToFileURL } from 'node:url';
import { resolve, join } from 'node:path';
import { mkdirSync } from 'node:fs';

const [kilde, udmappe] = process.argv.slice(2);
if (!kilde || !udmappe) {
  console.error('brug: node claude/hent_testfigurer.mjs <figurbilag.html> <udmappe>');
  process.exit(2);
}
mkdirSync(udmappe, { recursive: true });

const browser = await chromium.launch();
const page = await (await browser.newContext({
  viewport: { width: 900, height: 1000 }, deviceScaleFactor: 2,
})).newPage();
await page.goto(pathToFileURL(resolve(kilde)).href, { waitUntil: 'load' });
await page.waitForTimeout(300);

const figurer = await page.$$('figure');
if (!figurer.length) { console.error('ingen figurer fundet'); process.exit(1); }

for (const f of figurer) {
  const nr = await f.evaluate(e => e.id.replace('fig', ''));
  const navn = 'figur-' + String(nr).padStart(2, '0') + '.png';
  // kun selve tegningen med: billedteksten staar i spoergsmaalet i Forms
  const tegning = await f.$('.tegning');
  await tegning.screenshot({ path: join(udmappe, navn) });
}
console.log(figurer.length + ' figurer skrevet til ' + udmappe);
await browser.close();
