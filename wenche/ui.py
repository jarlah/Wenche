"""
Wenche — webgrensesnitt (Streamlit).

Start med: wenche ui
"""

import streamlit as st

from wenche.models import (
    Aarsregnskap,
    Aksjonaer,
    Aksjonaerregisteroppgave,
    Anleggsmidler,
    Balanse,
    Driftsinntekter,
    Driftskostnader,
    Egenkapital,
    EgenkapitalOgGjeld,
    Eiendeler,
    Finansposter,
    KortsiktigGjeld,
    LangsiktigGjeld,
    Omloepmidler,
    Resultatregnskap,
    Selskap,
    SkattemeldingKonfig,
)
from wenche import skattemelding as sm_modul
from wenche import aarsregnskap as ar_modul
from wenche import aksjonaerregister as akr_modul
from wenche.xbrl import generer_ixbrl

st.set_page_config(page_title="Wenche", layout="wide")
st.title("Wenche")
st.caption("Enkel innsending av regnskap og skattedokumenter til norske myndigheter")

fane_selskap, fane_regnskap, fane_aksjonaerer, fane_generer = st.tabs(
    ["🏢 Selskap", "📊 Regnskap og balanse", "👥 Aksjonærer", "📄 Generer"]
)


# ---------------------------------------------------------------------------
# Fane 1: Selskapsopplysninger
# ---------------------------------------------------------------------------

with fane_selskap:
    st.subheader("Selskapsopplysninger")
    col1, col2 = st.columns(2)
    with col1:
        navn = st.text_input("Selskapsnavn", value="Mitt Holding AS")
        org_nummer = st.text_input("Organisasjonsnummer (9 siffer)", value="123456789")
        daglig_leder = st.text_input("Daglig leder", value="Ola Nordmann")
        styreleder = st.text_input("Styreleder", value="Ola Nordmann")
    with col2:
        forretningsadresse = st.text_input(
            "Forretningsadresse", value="Gateveien 1, 0001 Oslo"
        )
        stiftelsesaar = st.number_input(
            "Stiftelsesår", min_value=1900, max_value=2100, value=2020
        )
        aksjekapital = st.number_input(
            "Aksjekapital (NOK)", min_value=0, value=30000, step=1000
        )
        regnskapsaar = st.number_input(
            "Regnskapsår", min_value=2000, max_value=2100, value=2025
        )


# ---------------------------------------------------------------------------
# Fane 2: Regnskap og balanse
# ---------------------------------------------------------------------------

with fane_regnskap:
    st.subheader("Resultatregnskap")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Driftsinntekter**")
        salgsinntekter = st.number_input(
            "Salgsinntekter", min_value=0, value=0, step=1000
        )
        andre_driftsinntekter = st.number_input(
            "Andre driftsinntekter", min_value=0, value=0, step=1000
        )
        sum_driftsinntekter = salgsinntekter + andre_driftsinntekter
        st.metric("Sum driftsinntekter", f"{sum_driftsinntekter:,} kr".replace(",", " "))

        st.markdown("**Driftskostnader**")
        loennskostnader = st.number_input(
            "Lønnskostnader", min_value=0, value=0, step=1000
        )
        avskrivninger = st.number_input(
            "Avskrivninger", min_value=0, value=0, step=1000
        )
        andre_driftskostnader = st.number_input(
            "Andre driftskostnader", min_value=0, value=5500, step=500
        )
        sum_driftskostnader = loennskostnader + avskrivninger + andre_driftskostnader
        st.metric("Sum driftskostnader", f"{sum_driftskostnader:,} kr".replace(",", " "))

        driftsresultat = sum_driftsinntekter - sum_driftskostnader
        st.metric("Driftsresultat", f"{driftsresultat:,} kr".replace(",", " "))

    with col2:
        st.markdown("**Finansposter**")
        utbytte_fra_datterselskap = st.number_input(
            "Utbytte fra datterselskap", min_value=0, value=0, step=1000
        )
        andre_finansinntekter = st.number_input(
            "Andre finansinntekter", min_value=0, value=0, step=1000
        )
        rentekostnader = st.number_input(
            "Rentekostnader", min_value=0, value=0, step=1000
        )
        andre_finanskostnader = st.number_input(
            "Andre finanskostnader", min_value=0, value=0, step=1000
        )
        resultat_foer_skatt = (
            driftsresultat
            + utbytte_fra_datterselskap
            + andre_finansinntekter
            - rentekostnader
            - andre_finanskostnader
        )
        st.metric(
            "Resultat før skatt", f"{resultat_foer_skatt:,} kr".replace(",", " ")
        )

    st.divider()
    st.subheader("Balanse")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Eiendeler**")
        st.markdown("*Anleggsmidler*")
        aksjer_i_datterselskap = st.number_input(
            "Aksjer i datterselskap", min_value=0, value=100000, step=1000
        )
        andre_aksjer = st.number_input("Andre aksjer", min_value=0, value=0, step=1000)
        langsiktige_fordringer = st.number_input(
            "Langsiktige fordringer", min_value=0, value=0, step=1000
        )
        sum_anleggsmidler = aksjer_i_datterselskap + andre_aksjer + langsiktige_fordringer

        st.markdown("*Omløpsmidler*")
        kortsiktige_fordringer = st.number_input(
            "Kortsiktige fordringer", min_value=0, value=0, step=1000
        )
        bankinnskudd = st.number_input(
            "Bankinnskudd", min_value=0, value=1200, step=100
        )
        sum_omloepmidler = kortsiktige_fordringer + bankinnskudd
        sum_eiendeler = sum_anleggsmidler + sum_omloepmidler
        st.metric("Sum eiendeler", f"{sum_eiendeler:,} kr".replace(",", " "))

    with col2:
        st.markdown("**Egenkapital og gjeld**")
        st.markdown("*Egenkapital*")
        ek_aksjekapital = st.number_input(
            "Aksjekapital (balanse)", min_value=0, value=30000, step=1000
        )
        overkursfond = st.number_input("Overkursfond", value=0, step=1000)
        annen_egenkapital = st.number_input(
            "Annen egenkapital (negativ ved underskudd)", value=-34300, step=1000
        )
        sum_egenkapital = ek_aksjekapital + overkursfond + annen_egenkapital

        st.markdown("*Langsiktig gjeld*")
        laan_fra_aksjonaer = st.number_input(
            "Lån fra aksjonær", min_value=0, value=105500, step=1000
        )
        andre_langsiktige_laan = st.number_input(
            "Andre langsiktige lån", min_value=0, value=0, step=1000
        )
        sum_langsiktig_gjeld = laan_fra_aksjonaer + andre_langsiktige_laan

        st.markdown("*Kortsiktig gjeld*")
        leverandoergjeld = st.number_input(
            "Leverandørgjeld", min_value=0, value=0, step=1000
        )
        skyldige_offentlige_avgifter = st.number_input(
            "Skyldige offentlige avgifter", min_value=0, value=0, step=1000
        )
        annen_kortsiktig_gjeld = st.number_input(
            "Annen kortsiktig gjeld", min_value=0, value=0, step=1000
        )
        sum_kortsiktig_gjeld = (
            leverandoergjeld + skyldige_offentlige_avgifter + annen_kortsiktig_gjeld
        )
        sum_ek_og_gjeld = sum_egenkapital + sum_langsiktig_gjeld + sum_kortsiktig_gjeld
        st.metric(
            "Sum egenkapital og gjeld", f"{sum_ek_og_gjeld:,} kr".replace(",", " ")
        )

    differanse = sum_eiendeler - sum_ek_og_gjeld
    if differanse == 0:
        st.success("Balansen stemmer")
    else:
        st.error(f"Balansen stemmer ikke. Differanse: {differanse:,} kr".replace(",", " "))


# ---------------------------------------------------------------------------
# Fane 3: Aksjonærer
# ---------------------------------------------------------------------------

with fane_aksjonaerer:
    st.subheader("Aksjonærer")
    antall = st.number_input("Antall aksjonærer", min_value=1, max_value=20, value=1)

    aksjonaerer_data = []
    for i in range(int(antall)):
        with st.expander(f"Aksjonær {i + 1}", expanded=(i == 0)):
            c1, c2 = st.columns(2)
            with c1:
                a_navn = st.text_input("Navn", key=f"a_navn_{i}", value="Ola Nordmann")
                a_fnr = st.text_input(
                    "Fødselsnummer (11 siffer)",
                    key=f"a_fnr_{i}",
                    value="01010112345",
                )
                a_aksjer = st.number_input(
                    "Antall aksjer", min_value=1, value=100, key=f"a_aksjer_{i}"
                )
            with c2:
                a_klasse = st.text_input(
                    "Aksjeklasse", key=f"a_klasse_{i}", value="ordinære"
                )
                a_utbytte = st.number_input(
                    "Utbytte utbetalt (NOK)",
                    min_value=0,
                    value=0,
                    key=f"a_utbytte_{i}",
                )
                a_kap = st.number_input(
                    "Innbetalt kapital per aksje (NOK)",
                    min_value=0,
                    value=300,
                    key=f"a_kap_{i}",
                )
            aksjonaerer_data.append((a_navn, a_fnr, a_aksjer, a_klasse, a_utbytte, a_kap))


# ---------------------------------------------------------------------------
# Fane 4: Generer dokumenter
# ---------------------------------------------------------------------------

with fane_generer:
    st.subheader("Generer dokumenter")

    st.markdown("**Skattemelding-innstillinger**")
    col1, col2 = st.columns(2)
    with col1:
        underskudd = st.number_input(
            "Fremførbart underskudd fra tidligere år (NOK)", min_value=0, value=0, step=1000
        )
    with col2:
        fritaksmetoden = st.checkbox(
            "Anvend fritaksmetoden",
            value=True,
            help="Sett til true for holdingselskaper som eier aksjer i datterselskaper",
        )

    st.divider()

    def bygg_regnskap() -> Aarsregnskap:
        return Aarsregnskap(
            selskap=Selskap(
                navn=navn,
                org_nummer=org_nummer,
                daglig_leder=daglig_leder,
                styreleder=styreleder,
                forretningsadresse=forretningsadresse,
                stiftelsesaar=int(stiftelsesaar),
                aksjekapital=int(aksjekapital),
            ),
            regnskapsaar=int(regnskapsaar),
            resultatregnskap=Resultatregnskap(
                driftsinntekter=Driftsinntekter(
                    salgsinntekter=int(salgsinntekter),
                    andre_driftsinntekter=int(andre_driftsinntekter),
                ),
                driftskostnader=Driftskostnader(
                    loennskostnader=int(loennskostnader),
                    avskrivninger=int(avskrivninger),
                    andre_driftskostnader=int(andre_driftskostnader),
                ),
                finansposter=Finansposter(
                    utbytte_fra_datterselskap=int(utbytte_fra_datterselskap),
                    andre_finansinntekter=int(andre_finansinntekter),
                    rentekostnader=int(rentekostnader),
                    andre_finanskostnader=int(andre_finanskostnader),
                ),
            ),
            balanse=Balanse(
                eiendeler=Eiendeler(
                    anleggsmidler=Anleggsmidler(
                        aksjer_i_datterselskap=int(aksjer_i_datterselskap),
                        andre_aksjer=int(andre_aksjer),
                        langsiktige_fordringer=int(langsiktige_fordringer),
                    ),
                    omloepmidler=Omloepmidler(
                        kortsiktige_fordringer=int(kortsiktige_fordringer),
                        bankinnskudd=int(bankinnskudd),
                    ),
                ),
                egenkapital_og_gjeld=EgenkapitalOgGjeld(
                    egenkapital=Egenkapital(
                        aksjekapital=int(ek_aksjekapital),
                        overkursfond=int(overkursfond),
                        annen_egenkapital=int(annen_egenkapital),
                    ),
                    langsiktig_gjeld=LangsiktigGjeld(
                        laan_fra_aksjonaer=int(laan_fra_aksjonaer),
                        andre_langsiktige_laan=int(andre_langsiktige_laan),
                    ),
                    kortsiktig_gjeld=KortsiktigGjeld(
                        leverandoergjeld=int(leverandoergjeld),
                        skyldige_offentlige_avgifter=int(skyldige_offentlige_avgifter),
                        annen_kortsiktig_gjeld=int(annen_kortsiktig_gjeld),
                    ),
                ),
            ),
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Generer skattemelding", use_container_width=True):
            regnskap = bygg_regnskap()
            konfig = SkattemeldingKonfig(
                underskudd_til_fremfoering=int(underskudd),
                anvend_fritaksmetoden=fritaksmetoden,
            )
            tekst = sm_modul.generer(regnskap, konfig)
            st.code(tekst, language=None)
            st.download_button(
                "Last ned skattemelding.txt",
                data=tekst.encode("utf-8"),
                file_name=f"skattemelding_{int(regnskapsaar)}_{org_nummer}.txt",
                mime="text/plain",
            )

    with col2:
        if st.button("Last ned iXBRL (årsregnskap)", use_container_width=True):
            regnskap = bygg_regnskap()
            feil = ar_modul.valider(regnskap)
            if feil:
                for f in feil:
                    st.error(f)
            else:
                ixbrl = generer_ixbrl(regnskap)
                st.download_button(
                    "Last ned årsregnskap.html",
                    data=ixbrl,
                    file_name=f"aarsregnskap_{int(regnskapsaar)}_{org_nummer}.html",
                    mime="application/xhtml+xml",
                )

    with col3:
        if st.button("Last ned RF-1086 XML", use_container_width=True):
            regnskap = bygg_regnskap()
            aksjonaerer = [
                Aksjonaer(
                    navn=a[0],
                    fodselsnummer=a[1],
                    antall_aksjer=int(a[2]),
                    aksjeklasse=a[3],
                    utbytte_utbetalt=int(a[4]),
                    innbetalt_kapital_per_aksje=int(a[5]),
                )
                for a in aksjonaerer_data
            ]
            oppgave = Aksjonaerregisteroppgave(
                selskap=regnskap.selskap,
                regnskapsaar=int(regnskapsaar),
                aksjonaerer=aksjonaerer,
            )
            feil = akr_modul.valider(oppgave)
            if feil:
                for f in feil:
                    st.error(f)
            else:
                xml = akr_modul.generer_xml(oppgave)
                st.download_button(
                    "Last ned aksjonaerregister.xml",
                    data=xml,
                    file_name=f"aksjonaerregister_{int(regnskapsaar)}_{org_nummer}.xml",
                    mime="application/xml",
                )
