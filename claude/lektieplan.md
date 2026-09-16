# Lektieplan · hvornår hvad udgives

Sidst opdateret: 2026-09-16

## Reglerne

1. **Lektier er altid åbne opgaver** — opgaver med bogstav og delspørgsmål
   a, b, c, bygget som modulopgaverne på klassens sider, men med andre tal.
2. **Multiple choice er ALDRIG lektier.** Quizzerne hører kun til som afslutning
   på modulerne på skoledelen. De er noget, ungerne selv kan øve sig på — i
   timen eller derhjemme — ikke noget der stilles for.
3. **Intet udgives før den dag, lektien gives.** Kommende lektier ligger i
   `kommende/` og udgives ved at flytte filen op i roden og pushe.
4. **Lektiearket uddeles som PDF uden facit.** PDF'erne ligger i `lektieark/`
   og hedder `lektier-<ÅÅÅÅ-MM-DD>-<emne>.pdf` — uden ordet "facit" i navnet.
   Mappen er udelukket fra deploy, så kommende ugers lektier ikke ligger frit.
5. **Facit kommer aldrig på sitet.** Facit ligger i `facit/` og sendes i Code.
   Begge mapper er udelukket i `.vercelignore`.
6. Besvarelsesformuleringen er altid:
   *"Lav udregninger i Word med Geogebra eller Excel og vis din metode."*

## Sådan udgives en lektie

```
git mv kommende/lektier-ugeNN-navn.html .
# tilføj et kort på matematik.html
git commit && git push
```

Vercel udgiver selv. Filen er live under et minut senere.

## Planen

Følger `aarsplan-matematik.html`. **Der laves ikke lektier ud over Manipulation
endnu** — aftalt 17. august 2026: indholdet skal beskrives, testes og
dokumenteres bedre først.

| Uge | Periode | Forløb | Fil | Status |
|---|---|---|---|---|
| 33 | 10.08 – 14.08 | Statistik: beskriv data | `lektier-uge33-beskriv-data.html` | ✅ udgivet |
| 34 | 17.08 – 21.08 | Statistik: diagrammer og sumkurve | `lektier-uge34-diagrammer.html` | ✅ udgivet |
| 35 | 24.08 – 28.08 | Manipulation | `kommende/lektier-uge35-manipulation.html` | ikke udgivet — ugen passerede |
| 36 | 31.08 – 04.09 | Manipulation (fortsat) | `lektier-uge36-manipulation-diagrammer.html` | ✅ udgivet 31.08 |
| 37 | 07.09 – 11.09 | Sandsynligheder i verden | — | ikke lavet, afventer |
| 38 | 14.09 – 18.09 | Ligninger og CAS | `lektier-uge38-ligninger.html` | ✅ udgivet 16.09 |
| 39 | 21.09 – 25.09 | Ligninger (fortsat) | `kommende/lektier-uge39-ligninger-cas.html` | klar, udgives når klassen er der |
| 41 | 05.10 – 09.10 | Lineære funktioner og grafer | `kommende/lektier-uge41-funktioner-grafer.html` | klar, udgives når klassen er der |

Uge 33 og 34 er udgivet samtidig, fordi uge 33 allerede var passeret, da lektierne
blev lavet.

## Udgivelse sker i hånden

**Lektier udgives ikke automatisk.** Klassens tempo svinger i forhold til
årsplanen, så det er læreren, der afgør hvornår en lektie gives. De Routines,
der udgav af sig selv, er slettet — de fyrede alligevel ikke pålideligt: uge 35,
36 og 38 måtte udgives i hånden.

I stedet kommer der en **mandagsmail**:

| Routine | Id | Fyrer |
|---|---|---|
| Mandagsmail · hvilke lektier ligger klar | `trig_01X2DGTRBWt12ZNRiuZUD8eo` | hver mandag kl. 06:00 UTC = 08:00 dansk, 07:00 om vinteren |

Mailen fortæller hvilken uge det er, hvad årsplanen siger, hvad der ligger klar
i `kommende/`, og hvad der sidst blev udgivet. **Den udgiver ingenting** — den
har direkte besked på hverken at flytte filer, committe eller pushe.

Skal en lektie ud, siger du det bare her i Code: filen flyttes op i roden,
kortet sættes på `matematik.html`, tjekket køres, og de to PDF'er sendes.

## Hvilken modulopgave svarer lektien til

Lektierne er bygget over modulopgaverne, så ungen møder samme opgavetype igen
med nye tal.

| Lektie | Bygget over |
|---|---|
| Uge 33, opgave A og B | `statistik.html`, Opgave A (modul 1) |
| Uge 34, opgave A og B | `statistik.html`, Opgave B (modul 2) |
| Uge 35, opgave A og B | `manipulation.html`, Opgave A og C |
| Uge 36, opgave A–D | `manipulation.html`, Opgave B og D |
| Uge 38, opgave A og B | `funktioner-og-ligninger.html`, Opgave A og B |
| Uge 39, opgave A–C | `funktioner-og-ligninger.html`, Opgave A (udvidet) |
| Uge 41, opgave A–C | `funktioner-og-ligninger.html`, Opgave C og D |

## Test af tallene

Tallene i lektierne er efterregnet programmatisk med brøkregning, ikke i
hovedet. Kravene der blev tjekket:

- Gennemsnit går op i et helt tal, hvor det er muligt.
- Frekvenser summer til præcis 100 %.
- Grader i cirkeldiagram summer til præcis 360°.
- Kumuleret frekvens ender på præcis 100 %.
- Kvartiler beregnet efter dansk skolemetode (median af hver halvdel, midterste
  observation udelades ved ulige antal).

Gør det samme, næste gang der laves lektier. Regn aldrig facit i hovedet.
