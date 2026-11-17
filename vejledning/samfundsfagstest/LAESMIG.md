# Samfundsfagstest · 60 spørgsmål til Microsoft Forms

Bygget af `claude/byg_forms_pakke.py`. Tallene er slået op 17. november 2026.

**Testen ligger ikke på 321flyv.com.** Øvelsessiden er bygget til
`kommende/samfundsfagstest.html`, som er udelukket fra deploy, og
rettenøglen ligger i `facit/`. Udgives noget af det, kan resultatet ikke
bruges til noget.

## Filerne

| Fil | Hvad den er til |
|---|---|
| `forms-import.docx` | Importeres i Forms. 60 spørgsmål, svar som a/b/c. Ingen billeder og ingen tabeller — det er med vilje, se nedenfor. |
| `figurbilag.pdf` | De 19 figurer, nummereret. Vedhæft den til opgaven, så eleverne har den åben ved siden af. |
| `figurer/figur-01.png` … `figur-19.png` | Samme figurer enkeltvis, hvis du hellere vil lægge dem ind i selve spørgsmålene. |
| `../../facit/facit-test-2026-11-17-samfundsfag60.pdf` | Rettenøgle: svarstrimmel med alle 60 bogstaver, og hvert spørgsmål med svar og forklaring. **Deles ikke med eleverne.** |

## Sådan gør du

1. Gå til <https://forms.office.com/>, og vælg **Hurtig import** (Quick
   Import) på forsiden. Findes knappen ikke, så opret en tom quiz, åbn
   **…**-menuen øverst til højre og vælg **Importer spørgsmål**.
2. Upload `forms-import.docx`, og vælg **Quiz** — ikke Formular. Kun en
   quiz kan give point og rette automatisk.
3. **Sæt det rigtige svar på hvert spørgsmål.** Importen henter ikke
   facit med. Brug svarstrimlen forrest i rettenøglen: 60 bogstaver i
   rækkefølge, så det er ét gennemløb.
4. Figurerne: enten vedhæft `figurbilag.pdf` til opgaven i Teams, eller
   læg billedet ind i hvert spørgsmål med billedknappen til højre for
   spørgsmålsteksten. Spørgsmålet siger selv, hvilket figurnummer det
   hører til.
5. I Teams: <https://teams.microsoft.com/> → dit hold → **Opgaver** →
   **Opret** → **Quiz** → vælg din Forms-quiz. Så afleverer eleverne den
   som en opgave, og du ser hvem der mangler.
6. Resultatet: åbn quizzen i Forms → **Svar** → **Åbn i Excel**. Der
   ligger hver elevs svar og point pr. spørgsmål.

## To ting, der er værd at vide på forhånd

- **Forms importerer ikke figurer.** Microsofts egen vejledning siger, at
  billeder og tabeller skal fjernes før import. Derfor står figurerne i et
  bilag i stedet for i filen, og derfor henviser hvert spørgsmål til et
  figurnummer.
- **Svarenes rækkefølge er den samme** i importfilen, i rettenøglen og på
  øvelsessiden. Slår Forms *Bland svarmuligheder* til, passer
  svarstrimlen ikke længere — lad den være slået fra.
