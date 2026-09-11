import pptxgen from 'pptxgenjs';
import fs from 'fs';
const SP = JSON.parse(fs.readFileSync('quizfig/quiz.json','utf8'));
const BIL = '/home/user/kontiki/facit/kahoot-billeder/';
const KAHOOT = ['E21B3C','1368CE','D89E00','26890C'];   // rød, blå, gul, grøn
const FORM   = ['triangle','diamond','circle','rectangle'];

const p = new pptxgen();
p.layout = 'LAYOUT_16x9';                                // 10 x 5.625 tommer
p.author = 'Mibelibsen · 9. klasse';
p.title  = 'Statistik · 30 spørgsmål';

// forside
const t = p.addSlide();
t.background = { color: '46178F' };
t.addText('Statistik', { x:0.7, y:1.5, w:8.6, h:1.0, isTextBox:true,
  fontFace:'Arial', fontSize:54, bold:true, color:'FFFFFF' });
t.addText('30 spørgsmål · 9. klasse', { x:0.7, y:2.6, w:8.6, h:0.6, isTextBox:true,
  fontFace:'Arial', fontSize:22, color:'E6DCFB' });
t.addText('Median og typetal · diagrammer · sumkurve · sandsynlighed · manipulation',
  { x:0.7, y:3.4, w:8.6, h:0.5, isTextBox:true, fontFace:'Arial', fontSize:14,
    color:'C9B6F5' });
t.addNotes('Facit står i noterne til hvert spørgsmål. Del ikke noterne med ungerne.');

for (const s of SP) {
  const sl = p.addSlide();
  sl.addText(`${s.nr}. ${s.q}`, { x:0.45, y:0.25, w:9.1, h:0.85, isTextBox:true,
    fontFace:'Arial', fontSize:18, bold:true, color:'1A2233', valign:'top',
    margin:0, shrinkText:true });
  sl.addImage({ path: BIL + s.png, x:0.9, y:1.15, w:8.2, h:2.45,
                sizing:{ type:'contain', w:8.2, h:2.45 } });
  s.sv.forEach((svar, j) => {
    const x = 0.45 + (j % 2) * 4.68, y = 3.78 + Math.floor(j / 2) * 0.78;
    sl.addShape(p.ShapeType.roundRect, { x, y, w:4.42, h:0.66,
      fill:{ color: KAHOOT[j] }, rectRadius:0.08 });
    sl.addText(svar, { x:x+0.16, y, w:4.1, h:0.66, isTextBox:true, fontFace:'Arial',
      fontSize:13, bold:true, color:'FFFFFF', valign:'middle', margin:0,
      shrinkText:true });
  });
  sl.addText(`${s.tid} sek.`, { x:8.55, y:5.18, w:1.0, h:0.3, isTextBox:true,
    fontFace:'Arial', fontSize:10, color:'8A93A6', align:'right', margin:0 });
  sl.addNotes(`Rigtigt svar: ${FORM[s.rigtig]} (${s.rigtig + 1}) — ${s.sv[s.rigtig]}`);
}
await p.writeFile({ fileName: '/home/user/kontiki/facit/kahoot-statistik-2026-09-11.pptx' });
console.log('slides:', SP.length + 1);
