/**
 * JUNG SEIN IN DEUTSCHLAND — det endelige spørgeskema (28.9.2026).
 *
 * Spørgsmålene står HER i scriptet, ikke i arket: gennemgået, uden dubletter,
 * tysken rettet, svarmuligheder sat på. Vil du rette et spørgsmål, så ret
 * i listen SPOERGSMAAL og kør igen.
 *
 * SÅDAN KØRES DET (5 minutter, ved en computer):
 *   1. Åbn arket med ungernes spørgsmål:
 *      https://docs.google.com/spreadsheets/d/1tV_rBMFwAtc8jQUXqP32TBOSEg52ZBQ05T-MIrfAK-Y/edit
 *   2. Menuen Udvidelser → Apps Script. Marker alt i editoren, slet det, og
 *      indsæt hele denne fil.
 *   3. Tryk Gem (disketten). Vælg funktionen "bygEndeligtSkema" i rullemenuen
 *      øverst, og tryk Kør. Sig ja til, at scriptet må bruge Forms og Sheets.
 *   4. Når det er kørt (10–20 sekunder), står der "Skema bygget" i loggen
 *      nederst, og fanen "Links" i arket har linkene.
 *
 * Skemaet beholder spørgsmålet "Code", så det forudfyldte link og alle
 * QR-kort virker uændret. Svar, der er kommet ind, røres ikke.
 */

const FORM_ID = '1_zEW7e1bvwL46TeywzPD9S3f8NzQ8CwDco62mWMWUgc';   // selve skemaet
const SVAR_ARK_ID = '1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY'; // svar + optælling

const TITEL = 'Jung sein in Deutschland';
const BESKRIVELSE =
  'Hallo! Wir sind eine 9. Klasse aus Dänemark. Wir sammeln Wissen darüber, ' +
  'wie es ist, in Deutschland jung zu sein, und vergleichen es damit, wie es ' +
  'ist, in Dänemark jung zu sein. Die Umfrage dauert nur ein paar Minuten. ' +
  'Alle Antworten sind anonym. Vielen Dank fürs Mitmachen!';
const TAK = 'Vielen Dank! Deine Antwort hilft uns, Deutschland und Dänemark zu vergleichen.';

// Svartyper:  jn = Ja/Nein · valg = vælg én (mulighederne i "valg")
//             tekst = kort svar (ikke påkrævet) · zahl = kun tal
// "af" er ungerne, spørgsmålet kommer fra — kun til jeres eget overblik.
const SPOERGSMAAL = [
  // --- Hamburg und Wohnen -------------------------------------------------
  { af: 'Ronja',  typ: 'jn',   frage: 'Wohnst du in Hamburg?' },
  { af: 'Johan',  typ: 'valg', frage: 'Wie lange wohnst du schon in Hamburg?',
    valg: ['Weniger als 1 Jahr', '1–5 Jahre', 'Mehr als 5 Jahre', 'Schon immer', 'Ich wohne nicht in Hamburg'] },
  { af: 'Clara',  typ: 'valg', frage: 'Mit wem wohnst du zusammen?',
    valg: ['Mit beiden Eltern', 'Mit einem Elternteil', 'Abwechselnd bei Mutter und Vater', 'Anders'] },
  { af: 'Flora · Nor', typ: 'tekst', frage: 'Was gefällt dir am besten an Hamburg?' },
  { af: 'Viktor', typ: 'tekst', frage: 'Welchen Ort in Hamburg würdest du uns für einen Besuch empfehlen?' },
  { af: 'Viktor · Flora', typ: 'valg', frage: 'Möchtest du auch später in Hamburg leben?',
    valg: ['Ja', 'Nein, woanders in Deutschland', 'Nein, im Ausland', 'Weiß ich noch nicht'] },

  // --- Schule und Arbeit --------------------------------------------------
  { af: 'Michael', typ: 'valg', frage: 'Gehst du zur Schule?',
    valg: ['Ja', 'Nein, ich mache eine Ausbildung', 'Nein, ich arbeite', 'Nein, etwas anderes'] },
  { af: 'Flora',  typ: 'tekst', frage: 'Was ist dein Lieblingsfach in der Schule?' },
  { af: 'Johan · William', typ: 'jn', frage: 'Hast du einen Nebenjob?' },
  { af: 'William', typ: 'tekst', frage: 'Welche Jobs kann man als junger Mensch in Hamburg machen?' },
  { af: 'Michael', typ: 'tekst', frage: 'Was ist dein Traumjob?' },

  // --- Freizeit und Freunde -----------------------------------------------
  { af: 'Oskar · Kasper · Ronja · Hjalte', typ: 'tekst', frage: 'Was machst du am liebsten in deiner Freizeit?' },
  { af: 'Nor',    typ: 'jn',   frage: 'Treibst du Sport?' },
  { af: 'Kasper', typ: 'jn',   frage: 'Machst du in deiner Freizeit Musik?' },
  { af: 'Nor',    typ: 'jn',   frage: 'Hast du ein Haustier?' },
  { af: 'Luna',   typ: 'jn',   frage: 'Gehst du oft ins Kino?' },
  { af: 'Hjalte', typ: 'valg', frage: 'Wie oft triffst du dich mit Freunden?',
    valg: ['Jeden Tag', 'Mehrmals pro Woche', 'Einmal pro Woche', 'Seltener'] },
  { af: 'Asta · Caroline', typ: 'valg', frage: 'Wohnen deine Freunde in Hamburg?',
    valg: ['Ja, alle', 'Die meisten', 'Etwa die Hälfte', 'Nur wenige'] },
  { af: 'Jonas',  typ: 'tekst', frage: 'Wo treffen sich Jugendliche in Hamburg?' },

  // --- Handy und Medien ---------------------------------------------------
  { af: 'Eksempel · Flora', typ: 'valg', frage: 'Wie viele Stunden am Tag bist du am Handy?',
    valg: ['Unter 1 Stunde', '1–2 Stunden', '3–4 Stunden', 'Mehr als 4 Stunden'] },
  { af: 'Asta',   typ: 'tekst', frage: 'Was machst du am liebsten mit deinem Handy?' },
  { af: 'Savanna', typ: 'valg', frage: 'Wie viele soziale Medien benutzt du?',
    valg: ['Keine', '1–2', '3–4', '5 oder mehr'] },
  { af: 'Savanna', typ: 'jn',  frage: 'Postest du gerne Fotos?' },
  { af: 'Kasper', typ: 'jn',   frage: 'Verfolgst du Trends im Internet?' },

  // --- Essen und Konsum ---------------------------------------------------
  { af: 'Clara · Caroline', typ: 'tekst', frage: 'Was ist dein deutsches Lieblingsgericht?' },
  { af: 'Luna',   typ: 'valg', frage: 'Wie oft pro Woche kaufst du Süßigkeiten?',
    valg: ['Nie', '1-mal', '2- bis 3-mal', '4-mal oder öfter'] },
  { af: 'Nor',    typ: 'jn',   frage: 'Magst du Bier?' },

  // --- Leben --------------------------------------------------------------
  { af: 'Jonas',  typ: 'tekst', frage: 'Was ist dir im Leben wichtig?' },
  { af: 'Milius', typ: 'tekst', frage: 'Was möchtest du im Leben unbedingt erleben?' },
  { af: 'Milius', typ: 'tekst', frage: 'Wenn du überall hinreisen könntest, wohin würdest du reisen?' },
  { af: 'Flora',  typ: 'tekst', frage: 'Was ist dein Lieblingsfilm?' },
];

// Baggrund til sidst (Silkes "Wie alt bist du?" ligger her).
const TIL_SIDST = [
  { frage: 'Wie alt bist du?', valg: ['13', '14', '15', '16', '17 oder älter'] },
  { frage: 'Bist du …', valg: ['ein Mädchen', 'ein Junge', 'divers', 'möchte ich nicht sagen'] },
];

function bygEndeligtSkema() {
  const form = FormApp.openById(FORM_ID);

  // Tøm skemaet, men behold "Code": så holder det forudfyldte link og QR-kortene.
  let code = null;
  form.getItems().forEach(i => {
    if (!code && i.getTitle() === 'Code' && i.getType() === FormApp.ItemType.TEXT) code = i.asTextItem();
    else form.deleteItem(i);
  });
  form.setTitle(TITEL).setDescription(BESKRIVELSE).setConfirmationMessage(TAK);
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(true);
  try { form.setRequireLogin(false); } catch (e) {}

  if (!code) code = form.addTextItem();
  code.setTitle('Code').setHelpText('Bitte nicht ändern.').setRequired(true);
  form.moveItem(code.getIndex(), 0);

  SPOERGSMAAL.forEach(s => {
    if (s.typ === 'jn') {
      form.addMultipleChoiceItem().setTitle(s.frage).setChoiceValues(['Ja', 'Nein']).setRequired(true);
    } else if (s.typ === 'valg') {
      if (!s.valg || s.valg.length < 2) throw new Error('"' + s.frage + '" mangler svarmuligheder.');
      form.addMultipleChoiceItem().setTitle(s.frage).setChoiceValues(s.valg).setRequired(true);
    } else if (s.typ === 'zahl') {
      const v = FormApp.createTextValidation().requireNumber().setHelpText('Bitte eine Zahl eingeben.').build();
      form.addTextItem().setTitle(s.frage).setValidation(v).setRequired(true);
    } else {
      form.addTextItem().setTitle(s.frage).setRequired(false);
    }
  });
  TIL_SIDST.forEach(s => form.addMultipleChoiceItem().setTitle(s.frage).setChoiceValues(s.valg).setRequired(true));

  // Svarene skal i regnearket, fanen "Svar".
  try { form.setDestination(FormApp.DestinationType.SPREADSHEET, SVAR_ARK_ID); } catch (e) {}
  const svarArk = SpreadsheetApp.openById(SVAR_ARK_ID);
  // Fanen, skemaet skriver i, skal hedde "Svar". Er den det allerede, røres
  // intet. Ellers får en gammel "Svar" et ledigt navn, og den nye omdøbes.
  const linked = svarArk.getSheets().filter(s => (s.getFormUrl() || '').indexOf(form.getId()) >= 0);
  if (linked.length && !linked.some(s => s.getName() === 'Svar')) {
    const gammel = svarArk.getSheetByName('Svar');
    if (gammel) {
      let navn = 'Svar (gammel)', k = 2;
      while (svarArk.getSheetByName(navn)) navn = 'Svar (gammel ' + k++ + ')';
      gammel.setName(navn);
    }
    linked[linked.length - 1].setName('Svar');
  }

  // Udgiv, og skriv linkene i fanen "Links".
  try { form.setPublished(true); } catch (e) {}
  try { form.setAcceptingResponses(true); } catch (e) {}
  const forudfyldt = form.createResponse().withItemResponse(code.createResponse('NAVN')).toPrefilledUrl();

  const ark = SpreadsheetApp.getActiveSpreadsheet() || svarArk;
  const links = ark.getSheetByName('Links') || ark.insertSheet('Links');
  links.clear();
  links.getRange(1, 1, 5, 2).setValues([
    ['Redigér skemaet', form.getEditUrl()],
    ['Link til dem der svarer', form.getPublishedUrl()],
    ['Forudfyldt link med NAVN', forudfyldt],
    ['Antal spørgsmål', String(SPOERGSMAAL.length + TIL_SIDST.length)],
    ['Bygget', new Date().toLocaleString('da-DK')],
  ]);
  links.autoResizeColumns(1, 2);
  Logger.log('Skema bygget: %s spørgsmål + Code + %s baggrundsspørgsmål.\nForudfyldt link: %s',
             SPOERGSMAAL.length, TIL_SIDST.length, forudfyldt);
}
