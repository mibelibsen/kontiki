// Bygger raadaekket til Pecha Kucha-skabelonen: 20 tomme slides i 16:9.
//
// Selve Pecha Kucha-reglen - at hvert slide staar praecis 20 sekunder og
// skifter af sig selv - kan pptxgenjs ikke skrive. Den saettes bagefter af
// claude/byg_pecha_kucha.py, som ogsaa laegger den tomme billedplads ind paa
// hvert slide. Koer det script, ikke dette.
// pptxgenjs ligger globalt og kan ikke slaas op med sit bare navn fra et
// ES-modul, saa den importeres med sin fulde sti - som playwright i
// claude/byg_bordplan.py. Mangler den: npm install -g pptxgenjs
import pptxgen from '/opt/node22/lib/node_modules/pptxgenjs/dist/pptxgen.es.js';

const SLIDES = 20;
const SEKUNDER = 20;
const UD = process.argv[2];
if (!UD) throw new Error('mangler filnavn som argument');

const p = new pptxgen();
p.layout = 'LAYOUT_16x9';                       // 10 x 5.625 tommer
p.author = 'Mibelibsen · 9. klasse';
p.title = 'Pecha Kucha · skabelon';
p.subject = `${SLIDES} slides a ${SEKUNDER} sekunder`;

// Ét layout: billedet fylder hele sliden. Der er ingen tekstfelter - teksten
// er det, man siger, og den staar i noterne.
p.defineSlideMaster({
  title: 'PECHAKUCHA',
  background: { color: '101418' },
  objects: [
    { placeholder: { options: { name: 'billede', type: 'pic',
                                x: 0, y: 0, w: 10, h: 5.625 }, text: '' } },
  ],
});

// 20 sekunder er ca. 45-50 ord i normalt taletempo (omkring 140 ord i minuttet).
const ORD = Math.round(140 / 60 * SEKUNDER);

for (let i = 1; i <= SLIDES; i++) {
  const s = p.addSlide({ masterName: 'PECHAKUCHA' });
  s.addNotes(
    `Slide ${i} af ${SLIDES} · ${SEKUNDER} sekunder · ca. ${ORD - 5}–${ORD} ord\n\n` +
    'Skriv her, hvad du siger til dette billede. Læs det højt med et ur: '
    + `bliver du ikke færdig på ${SEKUNDER} sekunder, skal der skæres ord væk — `
    + 'ikke tales hurtigere.');
}

await p.writeFile({ fileName: UD });
console.log(`raadaek skrevet: ${UD} · ${SLIDES} slides`);
