# Arbejdsregler for dette projekt

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

## Deploy

`main` er sandheden: det der ligger på `main`, ligger på mibelibsen.space.
Vercel deployer selv ved push. Se `claude/opsaetning.md`.

## Arbejdslog

Læs `claude/status-9klasse.md` først i en ny session, og opdatér den til sidst.
