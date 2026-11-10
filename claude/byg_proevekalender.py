# -*- coding: utf-8 -*-
"""Bygger vejledning/fp9-proever-januar-2027.ics til import i Outlook.

Bookingerne er skrevet af fra udtrækket paa booking.testogproever.dk.
**Listen giver kun starttidspunktet** - varighederne er UVM's officielle
proevetider, slaaet op, ikke husket:

  Matematik: de to dele afvikles i forlaengelse af hinanden uden pause,
             1 time uden hjaelpemidler + 3 timer med = 4 timer i alt
  Dansk, skriftlig fremstilling: 3,5 time
  Dansk, laesning og retskrivning: 1,5 time i alt
             (retskrivning 60 min, derefter laesning 30 min)

Filen skrives med CRLF og foldes paa 75 oktetter, som RFC 5545 kraever -
Outlook er kraesen med begge dele. Tidszonen ligger med i filen som en
VTIMEZONE, saa tiderne ikke flytter sig, hvis kalenderen staar i en anden
zone.

    python3 claude/byg_proevekalender.py
"""
import datetime as dt
import hashlib
import os

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROD, 'vejledning', 'fp9-proever-januar-2027.ics')
ZONE = 'Europe/Copenhagen'

KILDE = ('Skrevet af fra bookinglisten på booking.testogprøver.dk. Listen '
         'giver kun starttidspunktet; varigheden er UVM\u2019s officielle '
         'prøvetid.')

# (dato, booking som den staar i listen, titel, minutter, beskrivelse)
PROEVER = [
 ('2027-01-18', 'Matematik 8.kl', 'FP9 Matematik · 8. klasse', 240,
  'To prøver i forlængelse af hinanden, uden pause imellem:\n'
  '08:00–09:00  uden hjælpemidler (1 time)\n'
  '09:00–12:00  med hjælpemidler (3 timer)'),
 ('2027-01-19', 'Dansk 8.kl', 'FP9 Dansk, skriftlig fremstilling · 8. klasse',
  210, 'Samlet prøvetid 3½ time.\n08:00–11:30'),
 ('2027-01-20', 'Matematik 9.kl', 'FP9 Matematik · 9. klasse', 240,
  'To prøver i forlængelse af hinanden, uden pause imellem:\n'
  '08:00–09:00  uden hjælpemidler (1 time)\n'
  '09:00–12:00  med hjælpemidler (3 timer)'),
 ('2027-01-21', 'Dansk 9.kl', 'FP9 Dansk, skriftlig fremstilling · 9. klasse',
  210, 'Samlet prøvetid 3½ time.\n08:00–11:30'),
 ('2027-01-22', 'Dansk 9.kl', 'FP9 Dansk, læsning og retskrivning · 9. klasse',
  90, 'Samlet prøvetid 1½ time, digital selvrettende prøve:\n'
      '08:00–09:00  retskrivning (60 min)\n'
      '09:00–09:30  læsning (30 min)'),
]

START = dt.time(8, 0)


def _esc(s):
    """RFC 5545: omvendt skraastreg, semikolon, komma og linjeskift."""
    return (s.replace('\\', '\\\\').replace(';', '\;')
             .replace(',', '\\,').replace('\n', '\\n'))


def _fold(linje):
    """Maks 75 oktetter pr. linje. Der maa ikke brydes midt i et
    UTF-8-tegn, saa der taelles i bytes og brydes paa tegngraenser."""
    b = linje.encode('utf-8')
    if len(b) <= 75:
        return linje
    ud, rest, graense = [], b, 75
    while len(rest) > graense:
        skaer = graense
        while skaer > 0 and (rest[skaer] & 0xC0) == 0x80:   # midt i et tegn
            skaer -= 1
        ud.append(rest[:skaer].decode('utf-8'))
        rest = rest[skaer:]
        graense = 74                       # de foelgende linjer har et mellemrum
    ud.append(rest.decode('utf-8'))
    return '\r\n '.join(ud)


# Danmark: CET om vinteren, CEST fra sidste soendag i marts til sidste
# soendag i oktober. Reglerne skrives ind, saa filen ikke er afhaengig af,
# hvilke zoner modtagerens program kender.
VTIMEZONE = [
 'BEGIN:VTIMEZONE', f'TZID:{ZONE}',
 'BEGIN:STANDARD', 'DTSTART:19701025T030000',
 'RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU',
 'TZOFFSETFROM:+0200', 'TZOFFSETTO:+0100', 'TZNAME:CET', 'END:STANDARD',
 'BEGIN:DAYLIGHT', 'DTSTART:19700329T020000',
 'RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU',
 'TZOFFSETFROM:+0100', 'TZOFFSETTO:+0200', 'TZNAME:CEST', 'END:DAYLIGHT',
 'END:VTIMEZONE',
]


def byg():
    stempel = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    linjer = ['BEGIN:VCALENDAR', 'VERSION:2.0',
              'PRODID:-//9. klasse//FP9-proever januar 2027//DA',
              'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
              'X-WR-CALNAME:FP9-prøver januar 2027',
              f'X-WR-TIMEZONE:{ZONE}'] + VTIMEZONE
    for dato, booking, titel, minutter, tekst in PROEVER:
        d = dt.date.fromisoformat(dato)
        start = dt.datetime.combine(d, START)
        slut = start + dt.timedelta(minutes=minutter)
        noegle = f'{dato}-{booking}-{titel}'
        uid = hashlib.sha1(noegle.encode('utf-8')).hexdigest()[:16]
        linjer += [
            'BEGIN:VEVENT',
            f'UID:{uid}@fp9-2027',
            f'DTSTAMP:{stempel}',
            f'DTSTART;TZID={ZONE}:{start:%Y%m%dT%H%M%S}',
            f'DTEND;TZID={ZONE}:{slut:%Y%m%dT%H%M%S}',
            f'SUMMARY:{_esc(titel)}',
            f'DESCRIPTION:{_esc(tekst + chr(10) * 2 + "Booking: " + booking + chr(10) + KILDE)}',
            'CATEGORIES:FP9,Prøve',
            'TRANSP:OPAQUE',
            'X-MICROSOFT-CDO-BUSYSTATUS:BUSY',
            'END:VEVENT',
        ]
    linjer.append('END:VCALENDAR')
    return '\r\n'.join(_fold(l) for l in linjer) + '\r\n'


def _udfold(tekst):
    """Pakker foldningen ud igen - til kontrollen nedenfor."""
    return tekst.replace('\r\n ', '').replace('\r\n\t', '').split('\r\n')


if __name__ == '__main__':
    ics = byg()
    raa = _udfold(ics)
    assert raa.count('BEGIN:VEVENT') == len(PROEVER) == raa.count('END:VEVENT')
    assert all(len(l.encode('utf-8')) <= 75 for l in ics.split('\r\n')), \
        'en linje er længere end de 75 oktetter, RFC 5545 tillader'
    assert '\n' not in ics.replace('\r\n', ''), 'der er et nøgent linjeskift'
    assert ics.encode('utf-8').decode('utf-8') == ics
    for (dato, _b, _t, minutter, _tekst), s in zip(
            PROEVER, [l for l in raa if l.startswith('DTSTART;TZID=')]):
        assert s.endswith(dato.replace('-', '') + 'T080000'), s
    os.makedirs(os.path.dirname(UD), exist_ok=True)
    with open(UD, 'w', encoding='utf-8', newline='') as f:
        f.write(ics)
    print(f'skrevet:  {os.path.relpath(UD, ROD)}  ·  {len(PROEVER)} prøver')
    for dato, booking, titel, minutter, _ in PROEVER:
        d = dt.date.fromisoformat(dato)
        slut = (dt.datetime.combine(d, START)
                + dt.timedelta(minutes=minutter)).time()
        print(f'  {d:%a %d.%m.%Y}  {START:%H:%M}–{slut:%H:%M}  '
              f'({minutter // 60} t {minutter % 60:02d} min)  {titel}')
