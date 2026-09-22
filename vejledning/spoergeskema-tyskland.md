# Spørgeskemaet "Ung i Tyskland" · vejledning til den voksne

Sådan hænger det sammen, og hvad du selv skal gøre i Google. Det tager et
kvarter. Resten — koder, plakater, redirects og siden — bygger Claude med
`claude/byg_spoergeskema.py`, når du har sendt de to links.

## Sådan virker det

- **Ét spørgeskema** i Google Forms, ens for alle unger. Første spørgsmål
  hedder `Code` og bliver udfyldt automatisk af linket.
- **Hver ung har sin egen adresse** på sitet: `www.mibelibsen.space/u/anna-k`.
  Den sender videre til spørgeskemaet med ungens navn forudfyldt i `Code`.
  Den, der svarer, ser bare spørgeskemaet.
- **Alle svar lander i ét ark** — Google Forms' eget svar-ark. Kolonnen
  `Code` fortæller, hvis QR-kode svaret kom fra. Fanen `Unger` tæller
  pr. ung.
- **QR-koderne peger på sitet, ikke direkte på Google.** Så kan
  spørgeskemaet skiftes ud eller rettes, uden at plakaterne skal trykkes om.
  Man kan derfor godt trykke plakaterne, før spørgeskemaet er færdigt.
- **Forslag fra ungerne** kommer ind via en lille Google Form, som sender til
  det samme regneark (fanen `Forslag`). Den er linket fra
  https://www.mibelibsen.space/tysk-spoergeskema.html.

## Det Claude allerede har oprettet i dit Google Drev (22. september)

| Hvad | Link |
|---|---|
| Regnearket med fanen *Unger* og optællingen | https://docs.google.com/spreadsheets/d/1QwwgmHeMVc-lsMEtmXtT4BobkF0HGyjVr9Twi1tCWbY/edit |
| Forslagsformularen, tom | https://docs.google.com/forms/d/1DfEjbE50smAekXFi__JvAyzlV2vXOo4-yECYETSimJM/edit |
| Selve spørgeskemaet, tomt | https://docs.google.com/forms/d/1_zEW7e1bvwL46TeywzPD9S3f8NzQ8CwDco62mWMWUgc/edit |
| Teksterne til begge formularer, klar til at kopiere ind | https://docs.google.com/document/d/1h96ppA_vi6fnoye0KmNs5RWzKT5Zoh-YOCsrhBMM4TQ/edit |

Claudes Drev-adgang kan oprette dokumenter, regneark og tomme formularer, men
ikke skrive spørgsmål ind i en formular. Derfor ligger teksterne i et
dokument ved siden af.

## 1. Regnearket

Regnearket er lavet. Fanen *Unger* har navn, kode og QR-link for alle 23 og en
kolonne *Antal svar*, der tæller i fanen `Svar`, så snart den findes. Indtil da
er kolonnen tom. Det tomme ark *Tysk spørgeskema*, du selv oprettede, kan
slettes.

## 2. Forslagsformularen (til ungerne)

1. Åbn https://docs.google.com/forms/d/1DfEjbE50smAekXFi__JvAyzlV2vXOo4-yECYETSimJM/edit
2. Kopiér titel, beskrivelse og de fire spørgsmål ind fra dokumentet med
   teksterne: **Dit navn** (kort svar), **Dit spørgsmål på dansk** (afsnit),
   **Svarmuligheder** (kort svar), og et frivilligt *hvorfor*.
3. Fanen **Svar** øverst → ikonet *Link til Sheets* → **Vælg eksisterende
   regneark** → *Tysk spørgeskema – Unger og optælling*. Omdøb den nye fane i
   regnearket til `Forslag`.
4. Knappen **Send** → kæde-ikonet → **Kopiér**. Det er link nummer ét.

## 3. Selve spørgeskemaet (på tysk)

1. Åbn https://docs.google.com/forms/d/1_zEW7e1bvwL46TeywzPD9S3f8NzQ8CwDco62mWMWUgc/edit
   og kopiér titel og beskrivelse ind fra dokumentet med teksterne.
2. **Første spørgsmål: `Code`** — kort svar, *Påkrævet*, beskrivelse
   *Bitte nicht ändern*. Det er dét felt, linket fylder navnet i. Stav det
   præcis `Code`, for optællingen kigger efter kolonne B.
3. Herefter klassens spørgsmål — lukkede svar, ét emne ad gangen. Til sidst
   alder og køn. Eksempler står i dokumentet.
4. Fanen **Indstillinger** → *Svar*: slå **Begræns til 1 svar** FRA og
   **Indsaml e-mailadresser** FRA. Står der noget om at begrænse til brugere
   i organisationen, så slå det FRA — dem der svarer, er tyske unge uden
   login.
5. Fanen **Svar** → *Link til Sheets* → **Vælg eksisterende regneark** →
   *Tysk spørgeskema – Unger og optælling*. Omdøb fanen til `Svar`.
   Kolonne A er tidspunkt, kolonne B er `Code`. Fra det øjeblik tæller
   kolonnen *Antal svar* i fanen *Unger*.
6. **Linket med det forudfyldte felt:** de tre prikker øverst til højre →
   **Hent link med forudfyldte felter**. Skriv `NAVN` i feltet `Code`, tryk
   **Hent link** nederst og **Kopiér link**. Det er link nummer to. Det ser
   sådan ud:
   `https://docs.google.com/forms/d/e/…/viewform?usp=pp_url&entry.123456=NAVN`

Formularerne ligger altid samlet her: https://docs.google.com/forms/u/0/

## 4. Send til Claude

De to links. Claude sætter dem i `spoergeskema/opsaetning.json`, kører
scriptet og pusher. Navnene er allerede sat ind, og plakaterne er bygget:

| Fil | Hvad |
|---|---|
| `spoergeskema/qr-plakater-a4.pdf` | Én plakat pr. ung: QR, navn, tysk tekst, adressen i klartekst |
| `spoergeskema/qr-kort-a6.pdf` | Samme som kort, fire pr. A4-ark, klippes langs de stiplede linjer |
| `spoergeskema/unger-links.tsv` | Navn, kode og links — det samme som fanen `Unger` |

Mappen `spoergeskema/` udgives ikke. Kun koderne (`/u/anna`) står i
`vercel.json`, og de er alligevel trykt på plakaterne.

Skal der en ung til eller fra, eller får et spørgeskema nyt link: ret
listen, kør scriptet igen, push. Plakater, der allerede er trykt, virker
stadig, for koderne peger på sitet.

## 5. Optællingen i regnearket

Optællingen ligger i fanen *Unger*, kolonne *Antal svar*:

```
=IFERROR(COUNTIF(Svar!$B:$B; A2); "")
```

Den tæller, hvor mange rækker i `Svar` der har ungens navn i kolonne B, og
viser ingenting, så længe fanen `Svar` ikke findes. Nederst står `I alt`.

Vil du have **en fane pr. ung med ungens egne svar**, så lav en fane med
navnet og skriv i `A1`:

```
=FILTER(Svar!A:Z; Svar!B:B="Anna")
```

Så har alle den samme udgave af skemaet, og alle svar ligger stadig samlet
i `Svar`.

Et søjlediagram over optællingen: markér `A1:A24`, hold Ctrl nede og markér
`D1:D24` → **Indsæt** → **Diagram**.

## 6. Prøv det, før I tager af sted

1. Scan eksemplet på https://www.mibelibsen.space/tysk-spoergeskema.html —
   det fører tilbage til siden. Så virker sitet og redirects.
2. Scan én af de rigtige plakater og send et prøvesvar. Se, at rækken lander
   i `Svar` med det rigtige navn i kolonne B, og at *Antal svar* i fanen
   `Unger` viser 1.
3. Slet prøvesvaret i `Svar`, før det går løs.

## Hvis I skal bruge Microsoft Forms i stedet

Microsoft Forms kan ikke forudfylde et felt fra linket. Så skal der laves
én kopi af skemaet pr. ung, og hver kopi får sit eget link, som sættes i
`spoergeskema/opsaetning.json` — sig til, så laves scriptet om til det.
Svarene ligger så i ét Excel-ark pr. kopi og skal samles bagefter.
