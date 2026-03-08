# Installasjon

## Krav

- Python 3.11 eller nyere
- OpenSSL (følger med macOS og de fleste Linux-distribusjoner)

Sjekk Python-versjonen din:

```bash
python3 --version
```

Viser den 3.10 eller lavere, installer en nyere versjon:

=== "macOS"

    ```bash
    brew install python@3.11
    ```

=== "Linux (Ubuntu/Debian)"

    ```bash
    sudo apt install python3.11 python3.11-venv
    ```

=== "Windows"

    Last ned og installer fra [python.org](https://www.python.org/downloads/).

## Installer Wenche

Det anbefales å installere Wenche i et virtuelt miljø for å unngå konflikter med andre Python-pakker.

=== "Kommandolinje"

    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install wenche
    ```

=== "Webgrensesnitt"

    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install "wenche[ui]"
    ```

Wenche er nå tilgjengelig som kommandoen `wenche` i terminalen:

```bash
wenche --help
```

!!! tip "Husk å aktivere miljøet"
    Neste gang du åpner et nytt terminalvindu må du aktivere det virtuelle miljøet på nytt:
    ```bash
    source .venv/bin/activate
    ```

## Start webgrensesnittet

Har du installert `wenche[ui]`, starter du grensesnittet slik:

```bash
wenche ui
```

Streamlit starter og åpner `http://localhost:8501` i nettleseren. Åpnes ikke nettleseren automatisk, kan du lime inn adressen manuelt.

## For utviklere

Vil du bidra til koden eller kjøre siste versjon fra GitHub?

```bash
git clone https://github.com/olefredrik/wenche.git
cd wenche
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Kjør testsuiten:

```bash
pytest tests/ -v
```

[Gå videre til oppsett →](oppsett.md){ .md-button .md-button--primary }
