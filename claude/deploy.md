# Deploy · status og blokering

Sidst undersøgt: 2026-08-17

Læs denne fil **før** du prøver at deploye. Undersøgelsen nedenfor er lavet én
gang med rigtige API-kald; gentag den ikke fra bunden.

## Kort version

Jeg kan **ikke** deploye til mibelibsen.space. Vercel-forbindelsen i denne
session har ikke rettighederne, og den kan heller ikke se det projekt der
faktisk server domænet. Det er en konto-/rettighedssag, ikke noget der kan
rettes i koden.

## Hvad der er verificeret

**GitHub**

- `mibelibsen/kontiki` var **helt tomt** ved sessionens start — ingen commits,
  ingen brancher. Site­t kan derfor ikke have været deployet herfra.
- Brancher nu: `main` og `claude/status-9klasse-op6yol`, begge på samme commit.
- Repoets **default-branch er stadig `claude/status-9klasse-op6yol`**, fordi
  GitHub gør den første pushede branch til default. Der findes ingen MCP-tool
  til at ændre default-branch — det skal gøres manuelt under
  Settings → General → Default branch.
- Ingen af de øvrige repos (`kazzen-app`, `store51-pos`, `dog-lovers-app`,
  `dogloverstag`) er skolesitet.

**Vercel — team `mibelibsens-projects` (`team_mQu3h9xnYaeqpVu0FrqCK0QV`)**

`list_projects` giver fem projekter. Domænet `mibelibsen.space` sidder på
**ingen** af dem:

| Projekt | Domæner |
|---|---|
| kazzen-app | kazze.app, kazzen.app (+ www, + vercel.app) |
| dog-lovers-app | doglovers.app, dogloversapp.dk, dogloversapp.com (+ www) |
| s51pos-api | kun `*.vercel.app` |
| s51pos-mobil | kun `*.vercel.app` |
| s51pos-demo | kun `*.vercel.app` |

**De tre fejl der tilsammen udgør blokeringen**

1. Der findes allerede et projekt ved navn `kontiki`, men det er usynligt for
   mig. `create_git_project` med navnet `kontiki` svarer
   `409 conflict: Project "kontiki" already exists`, mens `get_project` på både
   team-id og team-slug svarer `404 Not Found`. Projektet ligger altså i en
   anden scope end den, min forbindelse læser fra — sandsynligvis den scope
   Claude Chat har deployet igennem i dag.
2. Forbindelsen må ikke deploye. `create_git_project` med navnet
   `kontiki-9klasse` oprettede projektet
   (`prj_WT1oGfW1ztnMBkYQ3tzH5Z4i1iup`), men deployet fejlede med
   `403 forbidden: You don't have permission to create a Production Deployment
   for this project`.
3. Forbindelsen kan ikke læse sine egne ting. `get_project` på det projekt jeg
   lige selv havde oprettet svarer `404`, og `list_deployments` svarer
   `403 forbidden: You don't have permission to list the deployment`.

Skrive- og læse-scope peger altså to forskellige steder hen. Det er derfor
forsøg på at automatisere deploys ser ud til at halvt lykkes hver gang.

**Netværk**

Selve sitet kan ikke hentes fra denne session — `curl` og `WebFetch` mod
`www.mibelibsen.space` blokeres af environmentets egress-proxy, og Vercels egen
`web_fetch_vercel_url` svarer `Unable to create shareable URL`. Sitets faktiske
indhold kan derfor ikke verificeres herfra.

## Oprydning

Projektet `kontiki-9klasse` (`prj_WT1oGfW1ztnMBkYQ3tzH5Z4i1iup`) blev oprettet
under undersøgelsen og har aldrig deployet noget. Det bør slettes i Vercel-
dashboardet. Der findes ingen MCP-tool til at slette projekter.

## Sådan låses det op

1. Find i Vercel-dashboardet hvilket projekt der har `mibelibsen.space` under
   Settings → Domains. Noter projektnavn og hvilken scope (personlig konto
   eller team) det ligger i.
2. Er projektet i din personlige konto og ikke i teamet `mibelibsens-projects`,
   så flyt det til teamet — ellers kan denne sessions forbindelse aldrig se det.
3. Giv Vercel-forbindelsen rollen **Member** eller **Owner** på det team.
   Rollen *Contributor* må ikke lave production-deploys, og det er præcis den
   fejl der kommer nu.
4. Kobl projektet til `mibelibsen/kontiki` under Settings → Git.
5. Sæt `main` som default-branch på GitHub, og som Production Branch i Vercel.
6. Slet `kontiki-9klasse`.

Når 1–6 er på plads, deployer et push til `main` automatisk til
mibelibsen.space, og jeg kan gøre resten herfra.

## Vigtigt før et fuldt deploy

Filerne i dette repo kommer fra en zip, der er et **ufuldstændigt** udtræk af
det live site. Konkret mangler `/style.css` og `/app.js`, som ligger på sitet.
Et deploy af repoet som det er nu vil derfor **fjerne** filer, der findes i dag,
og kan rulle nyere arbejde tilbage.

Inden første rigtige deploy: hent det live site ned, og sammenlign med repoet,
så repoet er et komplet billede. Ellers bliver deployet et tab, ikke en
opdatering.
