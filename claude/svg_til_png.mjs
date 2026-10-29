// Gengiver en SVG som PNG.
//   node claude/svg_til_png.mjs <kilde.html> <ud.png> <bredde> <hoejde>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const [k, u, b, h] = process.argv.slice(2);
const br = await chromium.launch();
const p = await br.newPage({ viewportSize: { width: +b, height: +h },
                             deviceScaleFactor: 3 });
await p.goto(pathToFileURL(resolve(k)).href, { waitUntil: 'load' });
await p.locator('svg').screenshot({ path: u });
await br.close();
