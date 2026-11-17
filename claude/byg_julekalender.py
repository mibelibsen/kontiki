# -*- coding: utf-8 -*-
"""Bygger CSV-filer til kalenderimport af skolens juleaktiviteter 2026.

Kilde: skolens seddel (foto, 17.11.2026). Teksten derfra staar ordret i
AKTIVITETER nedenfor.

**Aaret staar ikke paa sedlen.** Det er regnet frem af ugedagene: alle
fire datoer falder paa den ugedag, sedlen skriver, i 2026 — og paa ingen
af dem i 2025. Det tjekkes af en assert, saa filen ikke kan bygges med et
forkert aar.

Der udskrives to filer, fordi CSV-import laeser datoer forskelligt:
  - Outlook laeser datoer i Windows' danske format (dd-mm-aaaa)
  - Google Kalender kraever amerikansk format (mm/dd/aaaa)

    python3 claude/byg_julekalender.py
"""
import csv
import datetime
import os

HER = os.path.dirname(os.path.abspath(__file__))
UD = os.path.join(os.path.dirname(HER), 'vejledning')
DAGE = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']
AAR = 2026

# (ugedag paa sedlen, dato, titel, start, varighed i minutter, sted)
# start=None betyder, at sedlen ikke oplyser et klokkeslæt -> heldagspunkt.
AKTIVITETER = [
    ('Mandag', (11, 30), 'Juleklippedag', None, None, ''),
    ('Torsdag', (12, 3), 'KonTikis Venners julearrangement', None, None, ''),
    ('Fredag', (12, 11), 'Luciaoptog v. 0. kl.', (8, 30), 30, ''),
    ('Fredag', (12, 18), 'Julegudstjeneste', (9, 0), 60, 'Slotskirken'),
]
NOTE = 'Alle. Fra skolens seddel.'


def dato(md):
    return datetime.date(AAR, md[0], md[1])


# --- aaret kontrolleres mod ugedagene paa sedlen -------------------------
for ugedag, md, titel, *_ in AKTIVITETER:
    d = dato(md)
    assert DAGE[d.weekday()] == ugedag, (
        f'{d} er en {DAGE[d.weekday()]}, men sedlen skriver {ugedag} '
        f'for «{titel}» — er året {AAR} rigtigt?')
assert len(AKTIVITETER) == 4


def raekker(datoformat, heldag_tid):
    """En raekke pr. aktivitet. heldag_tid er det, der skrives i
    tidsfelterne for et heldagspunkt: Outlook vil have 00:00, Google vil
    hellere have dem tomme."""
    ud = []
    for ugedag, md, titel, start, minutter, sted in AKTIVITETER:
        d = dato(md)
        if start is None:
            t0 = t1 = heldag_tid
            heldag = 'True'
        else:
            s = datetime.datetime(d.year, d.month, d.day, *start)
            slut = s + datetime.timedelta(minutes=minutter)
            t0, t1 = s.strftime('%H:%M'), slut.strftime('%H:%M')
            heldag = 'False'
        ud.append([titel, d.strftime(datoformat), t0,
                   d.strftime(datoformat), t1, heldag, NOTE, sted])
    return ud


HOVED = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time',
         'All Day Event', 'Description', 'Location']


def skriv(filnavn, datoformat, heldag_tid, kodning):
    sti = os.path.join(UD, filnavn)
    # newline='' + CRLF: det format Outlook og Excel forventer af en CSV
    with open(sti, 'w', newline='', encoding=kodning) as f:
        w = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                       lineterminator='\r\n')
        w.writerow(HOVED)
        w.writerows(raekker(datoformat, heldag_tid))
    return sti


if __name__ == '__main__':
    # utf-8-sig: uden BOM viser Outlook og Excel æ, ø og å forkert
    a = skriv('juleaktiviteter-2026-outlook.csv', '%d-%m-%Y', '00:00',
              'utf-8-sig')
    b = skriv('juleaktiviteter-2026-google.csv', '%m/%d/%Y', '', 'utf-8')
    for sti in (a, b):
        print(f'skrevet: {os.path.relpath(sti)}')
    print()
    for ugedag, md, titel, start, minutter, sted in AKTIVITETER:
        d = dato(md)
        tid = f'kl. {start[0]}.{start[1]:02d} ({minutter} min)' if start \
            else 'hele dagen'
        print(f'  {ugedag} d. {d.day}.{d.month}.  {titel:34s} {tid}'
              + (f' · {sted}' if sted else ''))
