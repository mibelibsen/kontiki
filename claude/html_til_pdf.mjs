// Gengiver en HTML-fil som PDF med Chromium. Sidestoerrelsen tages fra
// sidens egen @page-regel, saa millimetermaal i CSS bliver millimeter paa
// papiret.
//
//   node claude/html_til_pdf.mjs <kilde.html> <ud.pdf> [skaermbillede.png]
//
// Playwright ligger i arbejdsmiljoeet under /opt/node22 og browseren under
// /opt/pw-browsers. Koer ikke `playwright install`.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const [kilde, ud, png] = process.argv.slice(2);
if (!kilde || !ud) {
  console.error('brug: node claude/html_til_pdf.mjs <kilde.html> <ud.pdf> [png]');
  process.exit(2);
}
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(pathToFileURL(resolve(kilde)).href, { waitUntil: 'load' });
await page.emulateMedia({ media: 'print' });
await page.pdf({ path: ud, preferCSSPageSize: true, printBackground: true });
if (png) {
  await page.setViewportSize({ width: 794, height: 1123 });   // A4 ved 96 dpi
  await page.screenshot({ path: png, fullPage: false });
}
await browser.close();
console.log(`skrevet:  ${ud}`);
