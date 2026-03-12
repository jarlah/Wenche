# Din første innsending

Denne veiledningen tar deg gjennom en komplett innsending fra start til slutt. Vi bruker et fiktivt selskap — **Fjordheim Holding AS** — som eksempel gjennom hele prosessen.

!!! note "Forutsetninger"
    Du bør ha fullført [installasjon](installasjon.md) og [oppsett](oppsett.md) før du starter. Wenche skal være installert, `.env` skal være konfigurert, og systembrukeren skal være godkjent i Altinn.

---

## Selskapet vi bruker som eksempel

**Fjordheim Holding AS** er et enkelt holdingselskap med følgende situasjon for regnskapsåret 2024:

- Eier 100 % av Fjordheim Teknologi AS
- Mottok **250 000 kr** i utbytte fra datterselskapet
- Betalte **5 500 kr** i regnskaps- og bankgebyrer
- Har **1 200 kr** på driftskonto per 31.12
- Aksjekapital: **30 000 kr**
- Daglig leder og styreleder: **Marte Fjordheim**
- Én aksjonær: Marte Fjordheim, 1 000 aksjer

---

## Steg 1 — Fyll ut config.yaml

Kopier eksempelfilen og åpne den i en teksteditor:

```bash
cp config.example.yaml config.yaml
```

Fyll inn tallene for Fjordheim Holding AS:

```yaml
selskap:
  navn: "Fjordheim Holding AS"
  org_nummer: "912345678"
  daglig_leder: "Marte Fjordheim"
  styreleder: "Marte Fjordheim"
  forretningsadresse: "Storgata 1, 5003 Bergen"
  stiftelsesaar: 2021
  aksjekapital: 30000

regnskapsaar: 2024

resultatregnskap:
  driftsinntekter:
    salgsinntekter: 0
    andre_driftsinntekter: 0
  driftskostnader:
    loennskostnader: 0
    avskrivninger: 0
    andre_driftskostnader: 5500
  finansposter:
    utbytte_fra_datterselskap: 250000
    andre_finansinntekter: 0
    rentekostnader: 0
    andre_finanskostnader: 0

balanse:
  eiendeler:
    anleggsmidler:
      aksjer_i_datterselskap: 100000
      andre_aksjer: 0
      langsiktige_fordringer: 0
    omloepmidler:
      kortsiktige_fordringer: 0
      bankinnskudd: 1200
  egenkapital_og_gjeld:
    egenkapital:
      aksjekapital: 30000
      overkursfond: 0
      annen_egenkapital: 213700
    langsiktig_gjeld:
      laan_fra_aksjonaer: 0
      andre_langsiktige_laan: 0
    kortsiktig_gjeld:
      leverandoergjeld: 0
      skyldige_offentlige_avgifter: 0
      annen_kortsiktig_gjeld: 52000

skattemelding:
  underskudd_til_fremfoering: 0
  anvend_fritaksmetoden: true
  eierandel_datterselskap: 100

aksjonaerer:
  - navn: "Marte Fjordheim"
    fodselsnummer: "01019012345"
    antall_aksjer: 1000
    aksjeklasse: "ordinære"
    utbytte_utbetalt: 0
    innbetalt_kapital_per_aksje: 30
```

!!! tip "Balansen må gå opp"
    Sum eiendeler (101 200 kr) skal være lik sum egenkapital og gjeld (30 000 + 213 700 + 52 000 = 295 700 kr)... Stemmer ikke? Wenche gir deg en advarsel og viser differansen. Dobbeltsjekk tallene.

---

## Steg 2 — Generer skattemeldingen

Skattemeldingen (RF-1167 + RF-1028) genereres lokalt og sendes inn manuelt på skatteetaten.no.

```bash
wenche generer-skattemelding
```

Du skal se en utskrift som inneholder:

- Næringsoppgave (RF-1167) med driftsinntekter, driftskostnader og finansposter
- Skatteberegning — for Fjordheim Holding AS med 100 % eierandel er utbyttet fritatt under fritaksmetoden, og skatten blir **0 kr**
- Egenkapitalnote (rskl. § 7-2b) — vises automatisk når `foregaaende_aar` er utfylt

Lagre til fil for enklere kopiering:

```bash
wenche generer-skattemelding --ut skattemelding_2024.txt
```

**Send inn manuelt:**

1. Gå til [skatteetaten.no](https://www.skatteetaten.no/) og logg inn med BankID
2. Åpne **Skattemelding for AS** for 2024
3. Fyll inn tallene fra sammendraget
4. Kontroller beregnet skatt og send inn

---

## Steg 3 — Test årsregnskapet (dry-run)

Før du sender inn, kan du se hva Wenche vil sende til Brønnøysundregistrene:

```bash
wenche send-aarsregnskap --dry-run
```

Dette genererer XML-dokumentene lokalt (`aarsregnskap_hovedskjema.xml` og `aarsregnskap_underskjema.xml`) uten å sende dem til Altinn. Nyttig for å verifisere at tallene er riktige.

---

## Steg 4 — Send årsregnskapet

```bash
wenche login
wenche send-aarsregnskap
wenche logout
```

Wenche laster opp årsregnskapet og skriver ut en lenke til Altinn når opplastingen er ferdig:

```
Årsregnskap lastet opp.
Signer her: https://tt02.altinn.no/ui/...
```

Åpne lenken i nettleseren og signer med BankID som daglig leder eller styreleder. Signeringen fullfører innsendingen.

!!! note "Signering skjer i Altinn, ikke i Wenche"
    Dette er et juridisk krav og kan ikke gjøres maskinelt.

---

## Steg 5 — Send aksjonærregisteroppgaven

```bash
wenche login
wenche send-aksjonaerregister
wenche logout
```

Aksjonærregisteroppgaven (RF-1086) sendes automatisk til Skatteetaten via Altinn. Ingen manuell signering nødvendig.

---

## Ferdig

Du har nå:

- [x] Generert og sendt inn skattemeldingen (RF-1167 + RF-1028)
- [x] Sendt inn årsregnskapet til Brønnøysundregistrene
- [x] Sendt inn aksjonærregisteroppgaven (RF-1086) til Skatteetaten

Neste år gjentar du fra steg 1 med oppdaterte tall — og husk å fylle ut `foregaaende_aar` med årets tall for å få med sammenligningstall (rskl. § 6-6).
