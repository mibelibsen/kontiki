# Arbejdsregler for dette projekt

**Den fulde dokumentation ligger i [`README.md`](README.md) i roden** — sitets
opbygning, filoversigt, deploy, quiz-motorens kontrakt, testkrav og hvad der
mangler. Læs den, før du ændrer noget. Nedenfor er kun de regler, der skal være
i hovedet hele tiden.

## Svar altid på dansk

Brugeren skriver dansk. Svar på dansk, også i commit-beskeder og dokumentation.

## ALTID DYBE LINKS

Når et svar beder brugeren om at gøre noget i en webgrænseflade — Vercel,
GitHub, et kontrolpanel — så giv **et direkte, klikbart link til præcis den
side**, hvor handlingen udføres. Aldrig "gå ind under Settings → Git". Altid
`https://vercel.com/<team>/<projekt>/settings/git`.

Det gælder hvert enkelt trin i en vejledning, ikke kun det første. Kender du
ikke et id eller projektnavn, så link til den liste, hvor brugeren selv finder
det — og sig hvad hen skal klikke på derfra.

Faste adresser i dette projekt:

- Vercel-team: `mibelibsens-projects`
- Vercel-dashboard: https://vercel.com/mibelibsens-projects
- Vercel-domæner: https://vercel.com/mibelibsens-projects/~/domains
- GitHub-repo: https://github.com/mibelibsen/kontiki

## Sitet

Statisk undervisningssite til 9. klasse. Rene HTML-filer, intet build, ingen
dependencies. Hver side er selvbærende: al CSS og JS ligger inline i filen, så
den virker alene. Hent aldrig CSS eller JS fra sitets rod — det var netop den
fejl, manipulation-siden havde.

Sproget på sitet er dansk. Eleverne omtales "unger".

## Facit og lektier

Facit kommer **aldrig** på sitet. Det ligger i `facit/` og sendes i Code.
Lektier er **altid** åbne opgaver — multiple choice er aldrig lektier. Intet
udgives før den dag, lektien gives; kommende lektier ligger i `kommende/`.
Begge mapper er udelukket i `.vercelignore`.

## ALTID VISUELLE EKSEMPLER

Hver opgave og hver forklaring skal have en figur. Et boksplot, en sumkurve, et
cirkeldiagram, et udfaldsrum, to søjler der viser procentpoint mod procent — en
tegning, ikke kun tal. Det gælder også facitlister: står der "tegn et boksplot"
i opgaven, skal facit **vise** boksplottet.

Byg dem med `claude/figurer.py`, som har færdige funktioner til de figurtyper,
sitet bruger. Tegn aldrig en figur på øjemål — koordinaterne skal beregnes.

## Kør tjekket før hvert push

```bash
python3 claude/tjek.py
```

Det fanger de fejl, der er sket før: facit der kan udgives, multiple choice i
lektier, sider der henter CSS fra roden, brudte links, manglende figurer, og
årsplanen der siger ét på siden og noget andet i regnearket. Ret alt der står
som FEJL, før du pusher.

## Regn altid efter

Regn aldrig facit i hovedet, og tegn aldrig figurer på øjemål. Brug
`fractions.Fraction`, og tjek at frekvenser giver 100 %, grader 360 %, og at
spørgsmålet faktisk har et svar. Se testafsnittet i `README.md`.

## Deploy

`main` er sandheden: det der ligger på `main`, ligger på mibelibsen.space.
Vercel deployer selv ved push. Brug ikke Vercels API — adgangen virker ikke og
skal ikke bruges. Se `claude/opsaetning.md`.

## Arbejdslog

Læs `claude/status-9klasse.md` først i en ny session, og opdatér den til sidst.
