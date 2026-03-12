# Din første innsending

Denne veiledningen tar deg gjennom en komplett innsending fra start til slutt. Vi bruker et fiktivt selskap — **Eksempel Holding AS** — som eksempel gjennom hele prosessen.

!!! note "Forutsetninger"
    Du bør ha fullført [installasjon](installasjon.md) og [oppsett](oppsett.md) før du starter. Wenche skal være installert, `.env` skal være konfigurert, og systembrukeren skal være godkjent i Altinn.

---

## Selskapet vi bruker som eksempel

**Eksempel Holding AS** er et enkelt holdingselskap med følgende situasjon for regnskapsåret 2024:

- Eier 100 % av Fjordheim Teknologi AS
- Mottok **250 000 kr** i utbytte fra datterselskapet
- Betalte **5 500 kr** i regnskaps- og bankgebyrer
- Har **1 200 kr** på driftskonto per 31.12
- Aksjekapital: **30 000 kr**
- Daglig leder og styreleder: **Kari Nordmann**
- Én aksjonær: Kari Nordmann, 1 000 aksjer

---

## Steg 1 — Fyll ut config.yaml

`config.example.yaml` i prosjektmappen er allerede fylt ut med tallene for Eksempel Holding AS. Kopier den for å følge denne veiledningen uten å endre noe:

```bash
cp config.example.yaml config.yaml
```

Når du er klar til å levere ditt eget regnskap, åpner du `config.yaml` i en teksteditor og erstatter verdiene med dine egne tall. Se [Referanse](referanse.md) for beskrivelse av alle felt.

!!! tip "Balansen må gå opp"
    Sum eiendeler skal være lik sum egenkapital og gjeld. Stemmer ikke tallene, gir Wenche deg en advarsel og viser differansen.

---

## Steg 2 — Generer skattemeldingen

Skattemeldingen (RF-1167 + RF-1028) genereres lokalt og sendes inn manuelt på skatteetaten.no.

```bash
wenche generer-skattemelding
```

Du skal se en utskrift som inneholder:

- Næringsoppgave (RF-1167) med driftsinntekter, driftskostnader og finansposter
- Skatteberegning — for Eksempel Holding AS med 100 % eierandel er utbyttet fritatt under fritaksmetoden, og skatten blir **0 kr**
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
