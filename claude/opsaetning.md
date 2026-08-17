# Opsætning af mibelibsen.space — én gang, så det bare kører

Sidst opdateret: 2026-08-17

## Hvorfor det er gået galt hele dagen

Sitet er indtil nu blevet deployet af Claude **gennem** Vercel. Den vej virker
ikke: adgangen til Vercel i chatten kan oprette ting, men hverken læse dem igen
eller udgive dem. Hvert forsøg lykkes derfor halvt, og næste forsøg starter
oven på noget halvfærdigt. Det er dét mønster, der har gentaget sig.

## Løsningen

Vi fjerner Claude fra deploy-leddet.

```
Claude  →  GitHub (mibelibsen/kontiki, branch main)  →  Vercel  →  mibelibsen.space
```

Vercel kobles til GitHub **én gang**. Derefter holder Vercel selv øje med
repoet: hver gang der kommer noget nyt på `main`, lægger den det op af sig selv,
typisk på under et minut. Claudes Vercel-adgang skal aldrig bruges igen, og
den fejl kan derfor ikke opstå.

## Sådan gør du — i denne rækkefølge

Rækkefølgen er vigtig. Sitet er oppe hele vejen igennem, og du sletter først
det gamle, når det nye beviseligt virker.

**1. Tjek at der ikke ligger noget på sitet, som ikke er i repoet.**
Åbn mibelibsen.space og klik rundt. Er der en side, der ikke findes i listen
nedenfor, så sig til, før du går videre — ellers forsvinder den.

Repoet indeholder: forside, matematik, samfundsfag, tysk, årsplan for matematik,
statistik, funktioner og ligninger, manipulation, hjemmeopgaver til statistik,
facitark til funktioner, samt fem PDF'er med lektier og facit.

**2. Lav et nyt projekt i Vercel.**
Vercel → *Add New* → *Project* → vælg GitHub-repoet `mibelibsen/kontiki`.
Framework: **Other**. Ingen build-kommando, ingen output-mappe — det er rene
HTML-filer, der bare skal serveres.

**3. Sæt `main` som Production Branch.**
Under projektets Settings → Git. Hvis feltet viser
`claude/status-9klasse-op6yol`, så ret det til `main`.

**4. Tjek at det virker.**
Vercel giver projektet en adresse i stil med `kontiki-xxxx.vercel.app`. Åbn den.
Ser sitet rigtigt ud, og virker quizzen på manipulation-siden? Så er du i mål.
Gå først videre, når det er bekræftet.

**5. Flyt domænet.**
Find det gamle projekt, der har `mibelibsen.space` under Settings → Domains.
Fjern domænet dér, og tilføj det på det nye projekt under Settings → Domains.
Tilføj både `mibelibsen.space` og `www.mibelibsen.space`.

**6. Ryd op.**
Slet nu det gamle projekt og projektet `kontiki-9klasse`, som blev oprettet
under fejlsøgningen og aldrig har udgivet noget.

**7. Ryd op på GitHub.**
Settings → General → Default branch → sæt til `main`. Slet derefter branchen
`claude/status-9klasse-op6yol`.

## Bagefter

Så er reglen enkel: **det, der ligger på `main`, er det, der ligger på sitet.**

Når du beder om en ændring, pusher jeg til `main`, og Vercel lægger den op selv.
Går noget galt, kan enhver ændring rulles tilbage i Vercel under *Deployments*
ved at vælge en tidligere version og trykke *Promote to Production*.

## Hvis noget alligevel driller

- **Ændringen kan ikke ses.** Tjek i Vercel under *Deployments*, om den nyeste
  er markeret *Ready* og *Production*. Ellers hold `Shift` og genindlæs siden —
  browseren kan have gemt den gamle udgave.
- **Siden er uden farver og layout.** Så mangler en fil. Alle sider i repoet er
  selvbærende, så det bør ikke kunne ske længere — det var netop den fejl,
  manipulation-siden havde.
- **Vercel bygger ikke ved et push.** Tjek at Production Branch stadig er `main`
  under Settings → Git.
