# Spørgeskemaet "Ung i Tyskland" · vejledning til den voksne

Sådan hænger det sammen, og hvad du selv skal gøre i Google. Det tager et
kvarter. Resten — koder, plakater, redirects og siden — bygger Claude med
`claude/byg_spoergeskema.py`, når du har sendt navnene og to links.

## Sådan virker det

- **Ét spørgeskema** i Google Forms, ens for alle unger. Første spørgsmål
  hedder `Code` og bliver udfyldt automatisk af linket.
- **Hver ung har sin egen adresse** på sitet: `www.mibelibsen.space/u/anna-k`.
  Den sender videre til spørgeskemaet med ungens navn forudfyldt i `Code`.
  Den, der svarer, ser bare spørgeskemaet.
- **Alle svar lander i ét ark** — Google Forms' eget svar-ark. Kolonnen
  `Code` fortæller, hvis QR-kode svaret kom fra. En fane `Optælling` tæller
  pr. ung.
- **QR-koderne peger på sitet, ikke direkte på Google.** Så kan
  spørgeskemaet skiftes ud eller rettes, uden at plakaterne skal trykkes om.
  Man kan derfor godt trykke plakaterne, før spørgeskemaet er færdigt.
- **Forslag fra ungerne** kommer ind via en lille Google Form, som sender til
  det samme regneark (fanen `Forslag`). Den er linket fra
  https://www.mibelibsen.space/tysk-spoergeskema.html.

## 1. Regnearket

1. Opret et nyt regneark: https://sheets.new — kald det fx *Ung i Tyskland*.
2. Lav en fane `Unger` (nederst: `+`). Den fyldes senere ved at indsætte
   indholdet af `spoergeskema/unger-links.tsv` — det falder selv i kolonner.

## 2. Forslagsformularen (til ungerne)

1. Opret en ny formular: https://forms.new — titel *Foreslå et spørgsmål*.
2. Tre spørgsmål: **Dit navn** (kort svar), **Dit spørgsmål på dansk**
   (afsnit), **Svarmuligheder** (kort svar, fx *Under 2 · 2–4 · Over 4*).
3. Fanen **Svar** øverst → ikonet *Link til Sheets* → **Vælg eksisterende
   regneark** → vælg *Ung i Tyskland*. Omdøb den nye fane i regnearket til
   `Forslag`.
4. Knappen **Send** → kæde-ikonet → **Kopiér**. Det er link nummer ét.

## 3. Selve spørgeskemaet (på tysk)

1. Ny formular: https://forms.new — titel fx *Jung sein in Deutschland*.
   Beskrivelse på tysk: hvem I er, at det er anonymt, at det tager få minutter.
2. **Første spørgsmål: `Code`** — kort svar, *Påkrævet*, beskrivelse
   *Bitte nicht ändern*. Det er dét felt, linket fylder navnet i. Stav det
   præcis `Code`, for optællingen kigger efter kolonnen.
3. Herefter klassens spørgsmål — lukkede svar, ét emne ad gangen. Til sidst
   alder og køn.
4. Fanen **Indstillinger** → *Svar*: slå **Begræns til 1 svar** FRA og
   **Indsaml e-mailadresser** FRA. Står der noget om at begrænse til brugere
   i organisationen, så slå det FRA — dem der svarer, er tyske unge uden
   login.
5. Fanen **Svar** → *Link til Sheets* → **Vælg eksisterende regneark** →
   *Ung i Tyskland*. Omdøb fanen til `Svar`. Kolonne A er tidspunkt,
   kolonne B er `Code`.
6. **Linket med det forudfyldte felt:** de tre prikker øverst til højre →
   **Hent link med forudfyldte felter**. Skriv `NAVN` i feltet `Code`, tryk
   **Hent link** nederst og **Kopiér link**. Det er link nummer to. Det ser
   sådan ud:
   `https://docs.google.com/forms/d/e/…/viewform?usp=pp_url&entry.123456=NAVN`

Formularerne ligger altid samlet her: https://docs.google.com/forms/u/0/

## 4. Send til Claude

Navnene (ét pr. linje) og de to links. Claude sætter dem i
`spoergeskema/unger.txt` og `spoergeskema/opsaetning.json`, kører scriptet,
pusher til `main` og sender:

| Fil | Hvad |
|---|---|
| `spoergeskema/qr-plakater-a4.pdf` | Én plakat pr. ung: QR, navn, tysk tekst, adressen i klartekst |
| `spoergeskema/qr-kort-a6.pdf` | Samme som kort, fire pr. A4-ark, klippes langs de stiplede linjer |
| `spoergeskema/unger-links.tsv` | Navn, kode og links — indsættes i fanen `Unger` |

Mappen `spoergeskema/` udgives ikke. Kun koderne (`/u/anna-k`) står i
`vercel.json`, og de er alligevel trykt på plakaterne.

Skal der en ung til eller fra, eller får et spørgeskema nyt link: ret
listen, kør scriptet igen, push. Plakater, der allerede er trykt, virker
stadig, for koderne peger på sitet.

## 5. Optællingen i regnearket

Lav fanen `Optælling`. Kolonne A: navnene, præcis som de står på
plakaterne (kopiér fra fanen `Unger`). I `B2`, og træk ned:

```
=COUNTIF(Svar!$B:$B; A2)
```

(Sheets viser den måske som `TÆL.HVIS`; semikolon mellem argumenterne i
dansk opsætning.) Nederst: `=SUM(B2:B40)` for det samlede antal.

Vil du have **en fane pr. ung med ungens egne svar**, så lav en fane med
navnet og skriv i `A1`:

```
=FILTER(Svar!A:Z; Svar!B:B="Anna K.")
```

Så har alle den samme udgave af skemaet, og alle svar ligger stadig samlet
i `Svar`.

Et søjlediagram over optællingen: markér `A1:B40` → **Indsæt** → **Diagram**.

## 6. Prøv det, før I tager af sted

1. Scan eksemplet på https://www.mibelibsen.space/tysk-spoergeskema.html —
   det fører tilbage til siden. Så virker sitet og redirects.
2. Scan én af de rigtige plakater og send et prøvesvar. Se, at rækken lander
   i `Svar` med det rigtige navn i kolonne B, og at `Optælling` tæller 1.
3. Slet prøvesvaret i `Svar`, før det går løs.

## Hvis I skal bruge Microsoft Forms i stedet

Microsoft Forms kan ikke forudfylde et felt fra linket. Så skal der laves
én kopi af skemaet pr. ung, og hver kopi får sit eget link, som sættes i
`spoergeskema/opsaetning.json` — sig til, så laves scriptet om til det.
Svarene ligger så i ét Excel-ark pr. kopi og skal samles bagefter.
