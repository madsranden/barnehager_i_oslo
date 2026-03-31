# Barnehageanalyse Oslo

Et verktøy for foreldre som vil ta et mer datadrevet valg av barnehage i Oslo.

Analysen kombinerer resultater fra Foreldreundersøkelsen (Udir) med avstand fra hjemadresse,
og gir en rangert liste og interaktivt kart over barnehagene.

**Dashbordet finner du her: [barnehageguiden.streamlit.app/](https://barnehageguiden.streamlit.app/)**

> **Merk:** Dette er i hovedsak et privat hobbyprosjekt laget i pappaperm for å opprettholde noen gamle
> Python-ferdigheter. Koden og analysen deles åpent i håp om at den kanskje kan være nyttig for andre,
> men prosjektet vedlikeholdes ikke aktivt.

## Datakilder

- **Foreldreundersøkelsen** – Lastet ned fra [Udir](https://www.udir.no/tall-og-forskning/statistikk/statistikk-barnehage/fuba-resultater-alle-sporsmal/). Foreldrene scorer barnehagen på en skala fra 1 til 5 på temaer som tilfredshet, barns medvirkning og lek.
- **Kartdata** – Hentet fra OpenStreetMap via [Overpass API](https://overpass-api.de/) for geolokasjon av barnehagene.

## Kjør dashbordet lokalt

1. Installer avhengigheter med [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```

2. Start dashbordet:
   ```bash
   uv run streamlit run dashboard.py
   ```

## Utforsk analysen

Vil du gå dypere kan du åpne `analyse.ipynb` i JupyterLab.

## Begrensninger

- Barnehager uten data fra Foreldreundersøkelsen er ikke med i analysen
- Det er ikke tatt hensyn til svarprosent eller statistisk usikkerhet
- Geografisk avstand tar ikke hensyn til reisevei eller kollektivtransport
