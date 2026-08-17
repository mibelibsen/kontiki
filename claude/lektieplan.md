# Lektieplan · hvornår hvad udgives

Sidst opdateret: 2026-08-17

## Reglerne

1. **Lektier er altid åbne opgaver** — opgaver med bogstav og delspørgsmål
   a, b, c, bygget som modulopgaverne på klassens sider, men med andre tal.
2. **Multiple choice er ALDRIG lektier.** Quizzerne hører kun til som afslutning
   på modulerne på skoledelen. De er noget, ungerne selv kan øve sig på — i
   timen eller derhjemme — ikke noget der stilles for.
3. **Intet udgives før den dag, lektien gives.** Kommende lektier ligger i
   `kommende/` og udgives ved at flytte filen op i roden og pushe.
4. **Facit kommer aldrig på sitet.** Facit ligger i `facit/` og sendes i Code.
   Begge mapper er udelukket i `.vercelignore`.
5. Besvarelsesformuleringen er altid:
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
| 35 | 24.08 – 28.08 | Manipulation | `kommende/lektier-uge35-manipulation.html` | ⏳ planlagt til 24.08 kl. 08.00 |
| 36 | 31.08 – 04.09 | Manipulation (fortsat) | `kommende/lektier-uge36-manipulation-diagrammer.html` | ⏳ planlagt til 31.08 kl. 08.00 |
| 37 | 07.09 – 11.09 | Sandsynligheder i verden | — | ikke lavet, afventer |

Uge 33 og 34 er udgivet samtidig, fordi uge 33 allerede var passeret, da lektierne
blev lavet.

## Planlagt udgivelse

Uge 35 og 36 udgives automatisk af to Routines, oprettet 17. august 2026. Begge
fyrer i en frisk session, uafhængigt af den samtale der oprettede dem, og sender
push og mail til ejeren når de er færdige.

| Uge | Id | Fyrer |
|---|---|---|
| 35 | `trig_01JHr8vUKSkFWdi6msBM5eMY` | 24.08.2026 kl. 06:00 UTC = 08:00 dansk |
| 36 | `trig_011VkD4eyGviV1DGpejiRHsa` | 31.08.2026 kl. 06:00 UTC = 08:00 dansk |

Hver af dem flytter sin fil op i roden, tilføjer kortet på `matematik.html`,
verificerer i browser, pusher til `main` og sender det tilhørende facit i chatten.

Routines kan ses og slettes med `list_triggers` og `delete_trigger`. Skal
udgivelsen aflyses eller flyttes, så ret eller slet den Routine — lav ikke en ny
ved siden af.

Bemærk: den fyrede session har ingen MCP-connectors, kun almindelige værktøjer.
Det er nok, fordi den bruger `git` direkte og ikke Vercels API.

## Hvilken modulopgave svarer lektien til

Lektierne er bygget over modulopgaverne, så ungen møder samme opgavetype igen
med nye tal.

| Lektie | Bygget over |
|---|---|
| Uge 33, opgave A og B | `statistik.html`, Opgave A (modul 1) |
| Uge 34, opgave A og B | `statistik.html`, Opgave B (modul 2) |
| Uge 35, opgave A og B | `manipulation.html`, Opgave A og C |
| Uge 36, opgave A–D | `manipulation.html`, Opgave B og D |

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
