# Facit · Lektier uge 33 og 34

**Må aldrig udgives på sitet.** Mappen `facit/` er udelukket i `.vercelignore`.

Alle tal er efterregnet programmatisk med brøkregning, så der ikke er
afrundingsfejl. Kvartiler er beregnet efter dansk skolemetode: medianen af den
nedre og den øvre halvdel, hvor midterste observation udelades ved ulige antal.

---

## Uge 33 · Beskriv data

### Opgave A — `4, 6, 6, 8, 9, 11, 12`

| | Svar | Udregning |
|---|---|---|
| a) Gennemsnit | **8** | 56 ÷ 7 = 8 |
| b) Median | **8** | 4. observation af 7 |
| b) Typetal | **6** | 6 optræder to gange |
| c) Variationsbredde | **8** | 12 − 4 = 8 |
| d) Q1 | **6** | median af `4, 6, 6` |
| d) Q3 | **11** | median af `9, 11, 12` |
| d) Kvartilbredde | **5** | 11 − 6 = 5 |
| e) Boksplot | **4 · 6 · 8 · 11 · 12** | min, Q1, median, Q3, max |

### Opgave B — `2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 18`

| | Svar | Udregning |
|---|---|---|
| a) Mindste / største | **2** og **18** | |
| b) Median | **9** | 6. observation af 11 |
| c) Q1 | **5** | median af `2, 3, 5, 6, 8` |
| c) Q3 | **13** | median af `10, 12, 13, 15, 18` |
| d) Boksplot | **2 · 5 · 9 · 13 · 18** | |
| e) Kvartilbredde | **8** | 13 − 5 = 8 |
| f) I kassen | **ca. 50 %** | Kassen går fra Q1 til Q3, altså midterste halvdel |

Til f): her ligger observationerne 5, 6, 8, 9, 10, 12, 13 — 7 af 11 — inde i
eller på kassen. Pointen ungerne skal nå frem til er, at kassen *per definition*
dækker den midterste halvdel; at det bliver 7 af 11 og ikke præcis 5,5 skyldes,
at Q1 og Q3 selv er observationer i en lille talrække.

---

## Uge 34 · Diagrammer og sumkurve

### Opgave A — transport, 25 unger

| Transport | Antal | Frekvens | Grader |
|---|---|---|---|
| Cykel | 10 | **40 %** | **144°** |
| Gang | 6 | **24 %** | **86,4°** |
| Bus | 7 | **28 %** | **100,8°** |
| Bil | 2 | **8 %** | **28,8°** |
| **I alt** | **25** | **100 %** | **360°** |

b) Typetallet er **Cykel**.

f) Med 30 unger kan man ikke sammenligne antal direkte — der skal sammenlignes
**frekvenser**. Et grupperet søjlediagram med procent på y-aksen er det rigtige
valg. To cirkeldiagrammer kan også bruges, men er sværere at sammenligne præcist.

### Opgave B — lektietid, 50 unger

| Minutter | Hyppighed | Kumuleret hyppighed | Kumuleret frekvens |
|---|---|---|---|
| 0–30 | 6 | **6** | **12 %** |
| 30–60 | 11 | **17** | **34 %** |
| 60–90 | 16 | **33** | **66 %** |
| 90–120 | 12 | **45** | **90 %** |
| 120–150 | 5 | **50** | **100 %** |

Aflæsninger på sumkurven (lineær interpolation i intervallet):

| | Svar | Ligger i intervallet |
|---|---|---|
| d) Median (50 %) | **75 min** | 60–90 |
| e) Q1 (25 %) | **ca. 48 min** | 30–60 |
| e) Q3 (75 %) | **ca. 101 min** | 90–120 |

Præcise værdier: Q1 = 47,73 min, Q3 = 101,25 min. Ungerne aflæser på egen
tegning, så alt mellem ca. 45–50 og ca. 98–105 bør godkendes.

f) **66 %** har under 90 minutter — læses direkte som den kumulerede frekvens
ved 90.
