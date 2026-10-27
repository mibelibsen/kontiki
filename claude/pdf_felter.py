# -*- coding: utf-8 -*-
"""Laegger udfyldelige tekstfelter ind i en faerdig PDF.

    python3.13 claude/pdf_felter.py <pdf> <felter.json>

felter.json er en liste af {"navn", "side", "rect": [llx, lly, urx, ury],
"flerlinje"}. Maalene er PDF-punkter med nulpunkt nederst til venstre, som
resten af PDF-verdenen regner i.

Kraever pypdf, som i denne container kun ligger under python3.13. Kald det
derfor gennem claude/byg_samtaleark.py, der selv finder en fortolker med
pypdf, i stedet for at gaette paa `python3`.
"""
import json
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject,
                           FloatObject, NameObject, NumberObject,
                           TextStringObject)

FLERLINJE = 1 << 12          # bit 13 i /Ff: feltet maa have linjeskift
SYNLIG = 4                   # bit 3 i /F: udskriv annotationen
SKRIFT = '/Helv 10 Tf 0 g'   # fast 10 pt: auto-skalering gjorde et navn kaempestort


def _felt(navn, rect, flerlinje):
    return DictionaryObject({
        NameObject('/Type'): NameObject('/Annot'),
        NameObject('/Subtype'): NameObject('/Widget'),
        NameObject('/FT'): NameObject('/Tx'),
        NameObject('/T'): TextStringObject(navn),
        NameObject('/V'): TextStringObject(''),
        NameObject('/Rect'): ArrayObject([FloatObject(v) for v in rect]),
        NameObject('/F'): NumberObject(SYNLIG),
        NameObject('/DA'): TextStringObject(
            SKRIFT),
        NameObject('/Ff'): NumberObject(FLERLINJE if flerlinje else 0),
        # Tom /MK: ingen ramme og ingen baggrund. Feltet skal ikke tegne
        # noget - stregerne staar allerede i selve sidens grafik.
        NameObject('/MK'): DictionaryObject({}),
    })


def paafoer(sti_pdf, felter, ud=None):
    laeser = PdfReader(sti_pdf)
    skriver = PdfWriter()
    skriver.append(laeser)

    skrifttype = skriver._add_object(DictionaryObject({
        NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'),
        NameObject('/BaseFont'): NameObject('/Helvetica'),
        NameObject('/Encoding'): NameObject('/WinAnsiEncoding'),
    }))

    navne = set()
    alle = []
    for f in felter:
        assert f['navn'] not in navne, f"to felter hedder {f['navn']}"
        navne.add(f['navn'])
        side = skriver.pages[f['side']]
        ref = skriver._add_object(_felt(f['navn'], f['rect'], f['flerlinje']))
        ref.get_object()[NameObject('/P')] = side.indirect_reference
        if '/Annots' in side:
            side[NameObject('/Annots')].append(ref)
        else:
            side[NameObject('/Annots')] = ArrayObject([ref])
        alle.append(ref)

    skriver._root_object[NameObject('/AcroForm')] = DictionaryObject({
        NameObject('/Fields'): ArrayObject(alle),
        # Uden NeedAppearances tegner en laeser ikke teksten, foer feltet har
        # vaeret redigeret én gang. Med den tegner den selv.
        NameObject('/NeedAppearances'): BooleanObject(True),
        NameObject('/DA'): TextStringObject(SKRIFT),
        NameObject('/DR'): DictionaryObject({
            NameObject('/Font'): DictionaryObject({
                NameObject('/Helv'): skrifttype,
            }),
        }),
    })
    skriver.write(ud or sti_pdf)
    return len(alle)


if __name__ == '__main__':
    pdf, spec = sys.argv[1], sys.argv[2]
    n = paafoer(pdf, json.load(open(spec, encoding='utf-8')))
    print(f'{n} felter')
