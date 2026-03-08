# Wenche

Wenche er et verktøy for holdingselskaper og småaksjeselskaper som må levere regnskap og skattedokumenter til norske myndigheter. Det kan brukes både fra kommandolinjen og via et grafisk webgrensesnitt — uten behov for et fullverdig regnskapsprogram.

Autentisering skjer via Maskinporten med et selvgenerert RSA-nøkkelpar. Ingen virksomhetssertifikat eller BankID-innlogging nødvendig.

## Hva hjelper Wenche med?

Alle AS plikter å levere tre ting hvert år:

| Hva | Til hvem | Frist | Status |
|---|---|---|---|
| **Årsregnskap** | Brønnøysundregistrene | 31. juli | Automatisk innsending |
| **Aksjonærregisteroppgave** (RF-1086) | Skatteetaten via Altinn | 31. januar | Automatisk innsending |
| **Skattemelding for AS** (RF-1028 + RF-1167) | Skatteetaten | 31. mai | Genereres lokalt — sendes inn manuelt |

!!! info "Om skattemeldingen"
    Automatisk innsending av skattemelding krever registrering som systemleverandør hos Skatteetaten. Wenche genererer i stedet et ferdig utfylt sammendrag som du kopierer inn på skatteetaten.no.

## Hva er de ulike skjemaene?

- **Årsregnskapet** er en oppsummering av selskapets økonomi — hva selskapet eier, hva det skylder, og hva det tjente eller tapte i løpet av året. Dette er offentlig informasjon.
- **Aksjonærregisteroppgaven (RF-1086)** forteller Skatteetaten hvem som eier aksjer i selskapet og om det er utbetalt utbytte. Brukes blant annet til å forhåndsutfylle aksjonærenes personlige skattemelding.
- **Næringsoppgaven (RF-1167)** er en detaljert oppstilling av selskapets inntekter og kostnader for skatteformål, og er grunnlaget for skatteberegningen.
- **Skattemeldingen for AS (RF-1028)** er selve skattemeldingen. For holdingselskaper gjelder **fritaksmetoden**: utbytte fra datterselskaper er i praksis 97 % skattefritt.

## Kom i gang

[Installasjon →](installasjon.md){ .md-button .md-button--primary }
[Oppsett →](oppsett.md){ .md-button }
