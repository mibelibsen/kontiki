/**
 * Bygger spørgeskemaet "Jung sein in Deutschland" i Google Forms
 * af arket "Ung i Tyskland – jeres spørgsmål".
 *
 * SÅDAN (én gang, ved en computer):
 *   1. Åbn arket med ungernes spørgsmål:
 *      https://docs.google.com/spreadsheets/d/1tV_rBMFwAtc8jQUXqP32TBOSEg52ZBQ05T-MIrfAK-Y/edit
 *   2. Menuen Udvidelser → Apps Script. Slet det, der står, og indsæt hele denne fil.
 *   3. Tryk Gem (disketten), vælg funktionen "bygSkema" i rullemenuen, tryk Kør.
 *      Første gang spørger Google om lov — vælg din konto, "Avanceret",
 *      "Gå til … (usikker)", Tillad. Det er dit eget script på din egen konto.
 *   4. Når det er kørt, ligger der en ny fane "Links" i arket med:
 *        - linket til at redigere skemaet
 *        - linket ungerne/tyskerne åbner
 *        - linket med det forudfyldte felt, hvor der står NAVN — det sendes til Claude.
 *
 * Scriptet kan køres igen, når spørgsmålene er rettet: det tømmer skemaet og
 * bygger det forfra. Svar, der allerede er kommet ind, ligger i regnearket og
 * røres ikke.
 *
 * HVILKE LINJER KOMMER MED: alle linjer med et spørgsmål, undtagen "Eksempel".
 * Vil I vælge ud, så lav en kolonne med overskriften "Med" og sæt et x i de
 * linjer, der skal med — så tages kun dem.
 *
 * SVARTYPER (kolonnen Antworttyp, store/små bogstaver er ligegyldige):
 *   Ja/Nein       → multiple choice: Ja · Nein
 *   Auswahl       → multiple choice med mulighederne fra næste kolonne,
 *                   adskilt af · , ; / eller linjeskift
 *   Skala 1–5     → lineær skala (tallene læses fra teksten, fx "Skala 1–10")
 *   Zahl          → kort svar, kun tal
 *   Freier Text   → afsnit (ikke påkrævet)
 */

// Skemaet, der skal fyldes (tomt, oprettet 22.9.). Tom streng = lav et nyt.
const FORM_ID = '1_zEW7e1bvwL46TeywzPD9S3f8NzQ8CwDco62mWMWUgc';
// Regnearket, svarene skal lande i (fanen "Unger" tæller i fanen "Svar").
const SVAR_ARK_ID = '1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY';

const TITEL = 'Jung sein in Deutschland';
const BESKRIVELSE =
  'Hallo! Wir sind eine 9. Klasse aus Dänemark. Wir sammeln Wissen darüber, ' +
  'wie es ist, in Deutschland jung zu sein, und vergleichen es damit, wie es ' +
  'ist, in Dänemark jung zu sein. Die Umfrage dauert nur ein paar Minuten. ' +
  'Alle Antworten sind anonym. Vielen Dank fürs Mitmachen!';
const TAK = 'Vielen Dank! Deine Antwort hilft uns, Deutschland und Dänemark zu vergleichen.';

// Baggrundsspørgsmål til sidst. Sæt til [] for at droppe dem.
const TIL_SIDST = [
  { tekst: 'Wie alt bist du?', valg: ['13', '14', '15', '16', '17 oder älter'] },
  { tekst: 'Bist du …', valg: ['ein Mädchen', 'ein Junge', 'divers', 'möchte ich nicht sagen'] },
];

function bygSkema() {
  const ark = SpreadsheetApp.getActiveSpreadsheet();
  const linjer = laesSpoergsmaal_(ark.getSheets()[0]);
  if (!linjer.length) throw new Error('Der er ingen spørgsmål i arket (ud over eksemplet).');

  // --- skemaet -----------------------------------------------------------
  const form = FORM_ID ? FormApp.openById(FORM_ID) : FormApp.create(TITEL);
  form.getItems().forEach(i => form.deleteItem(i));       // tøm, så det kan køres igen
  form.setTitle(TITEL).setDescription(BESKRIVELSE).setConfirmationMessage(TAK);
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  try { form.setRequireLogin(false); } catch (e) {}       // findes kun på skolekonti

  // 1) Code — udfyldes af linket, tæller svaret på den rigtige ung
  const code = form.addTextItem().setTitle('Code').setHelpText('Bitte nicht ändern.').setRequired(true);

  // 2) klassens spørgsmål
  linjer.forEach(l => tilfoej_(form, l));

  // 3) baggrund
  TIL_SIDST.forEach(s => form.addMultipleChoiceItem().setTitle(s.tekst).setChoiceValues(s.valg).setRequired(true));

  // --- svarene til regnearket, fanen "Svar" -----------------------------
  try { form.setDestination(FormApp.DestinationType.SPREADSHEET, SVAR_ARK_ID); } catch (e) {}
  const svarArk = SpreadsheetApp.openById(SVAR_ARK_ID);
  const formUrl = form.getEditUrl().replace(/\/edit.*$/, '');
  svarArk.getSheets().forEach(s => {
    const u = s.getFormUrl();
    if (u && u.indexOf(form.getId()) >= 0 && s.getName() !== 'Svar') {
      if (svarArk.getSheetByName('Svar')) svarArk.getSheetByName('Svar').setName('Svar (gammel)');
      s.setName('Svar');
    }
  });

  // --- udgiv og lav linkene ---------------------------------------------
  try { form.setPublished(true); } catch (e) {}          // nye Forms skal udgives
  try { form.setAcceptingResponses(true); } catch (e) {}
  const forudfyldt = form.createResponse()
    .withItemResponse(code.createResponse('NAVN'))
    .toPrefilledUrl();

  let links = ark.getSheetByName('Links') || ark.insertSheet('Links');
  links.clear();
  links.getRange(1, 1, 5, 2).setValues([
    ['Redigér skemaet', form.getEditUrl()],
    ['Link til dem der svarer', form.getPublishedUrl()],
    ['Forudfyldt link med NAVN — send til Claude', forudfyldt],
    ['Antal spørgsmål fra arket', String(linjer.length)],
    ['Bygget', new Date().toLocaleString('da-DK')],
  ]);
  links.autoResizeColumns(1, 2);
  Logger.log('Skema bygget med %s spørgsmål.\nForudfyldt link: %s', linjer.length, forudfyldt);
}

// ---------------------------------------------------------------- hjælpere
function laesSpoergsmaal_(sheet) {
  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];
  const hoved = data[0].map(h => String(h).trim().toLowerCase());
  const kol = navn => hoved.findIndex(h => h.startsWith(navn));
  const iNavn = kol('navn'), iFrage = kol('deine frage'), iTyp = kol('antworttyp'),
        iValg = kol('antwortmög'), iMed = kol('med');
  if (iFrage < 0 || iTyp < 0) throw new Error('Arket mangler kolonnerne "Deine Frage" og/eller "Antworttyp".');
  const brugMed = iMed >= 0 && data.slice(1).some(r => String(r[iMed]).trim());
  return data.slice(1)
    .map(r => ({
      navn: String(r[iNavn] || '').trim(),
      frage: String(r[iFrage] || '').trim(),
      typ: String(r[iTyp] || '').trim().toLowerCase(),
      valg: String(iValg >= 0 ? r[iValg] || '' : '').trim(),
      med: iMed >= 0 ? String(r[iMed] || '').trim() : '',
    }))
    .filter(l => l.frage && l.navn.toLowerCase() !== 'eksempel' && (!brugMed || l.med));
}

function tilfoej_(form, l) {
  const t = l.typ;
  if (t.startsWith('ja')) {
    form.addMultipleChoiceItem().setTitle(l.frage).setChoiceValues(['Ja', 'Nein']).setRequired(true);
  } else if (t.startsWith('auswahl') || t.startsWith('valg')) {
    const valg = l.valg.split(/[·,;/\n]/).map(s => s.trim()).filter(Boolean);
    if (valg.length < 2) throw new Error('Spørgsmålet "' + l.frage + '" er Auswahl, men har under to svarmuligheder.');
    form.addMultipleChoiceItem().setTitle(l.frage).setChoiceValues(valg).setRequired(true);
  } else if (t.startsWith('skala')) {
    const tal = t.match(/\d+/g) || [];
    const lo = tal.length > 1 ? Number(tal[0]) : 1;
    const hi = tal.length ? Number(tal[tal.length - 1]) : 5;
    form.addScaleItem().setTitle(l.frage).setBounds(lo, hi).setRequired(true);
  } else if (t.startsWith('zahl') || t.startsWith('tal')) {
    const v = FormApp.createTextValidation().requireNumber().setHelpText('Bitte eine Zahl eingeben.').build();
    form.addTextItem().setTitle(l.frage).setValidation(v).setRequired(true);
  } else if (t.startsWith('frei') || t.startsWith('fri')) {
    form.addParagraphTextItem().setTitle(l.frage).setRequired(false);
  } else {
    form.addTextItem().setTitle(l.frage).setHelpText('(Antworttyp "' + l.typ + '" ukendt — kort svar)').setRequired(false);
  }
}
