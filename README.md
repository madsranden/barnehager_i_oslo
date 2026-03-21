# Barnehageanalyse Oslo

Et verktøy for foreldre som vil ta et mer datadrevet valg av barnehage i Oslo.

Analysen kombinerer resultater fra Foreldreundersøkelsen (Udir) med avstand fra hjemadresse,
og gir en rangert liste og interaktivt kart over barnehagene.

> **Merk:** Dette er i hovedsak et privat hobbyprosjekt laget i pappaperm for å opprettholde noen gamle
> Python-ferdigheter. Koden og analysen deles åpent i håp om at den kanskje kan være nyttig for andre,
> men prosjektet vedlikeholdes ikke aktivt. 

## Datakilder

- **Foreldreundersøkelsen** – Lastet ned fra [Udir](https://www.udir.no/tall-og-forskning/statistikk/statistikk-barnehage/fuba-resultater-alle-sporsmal/). Foreldrene scorer barnehagen på en skala fra 1 til 5 på temaer som tilfredshet, barns medvirkning og lek.
- **Kartdata** – Hentet fra OpenStreetMap via [Overpass API](https://overpass-api.de/) for geolokasjon av barnehagene.

## Slik bruker du analysen

1. Installer avhengigheter med [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```

2. Rens og forbered data:
   ```bash
   uv run python rense_data.py
   uv run python barnehage_id.py
   ```

3. Åpne `analyse.ipynb` i JupyterLab og tilpass disse variablene øverst i notatboken:

   ```python
   år = 2023              # Tilgjengelige år: 2023, 2025, 2026
   hjem_adresse = "Hedmarksgata 4"
   vekt_undersokelse = 0.3  # 0.3 = 30 % vekt på undersøkelsen, 70 % på avstand
   ```

4. Kjør alle celler.

## Hva analysen gjør

- Sammenstiller alle spørsmål fra Foreldreundersøkelsen og lager en samlet score per barnehage
- Beregner avstand (i meter) fra hjemadresse til hver barnehage
- Kombinerer avstand og undersøkelsesscore til en **total score** basert på valgfri vekting

## Begrensninger

- Barnehager uten data fra Foreldreundersøkelsen er ikke med i analysen
- Det er ikke tatt hensyn til svarprosent eller statistisk usikkerhet
- Geografisk avstand tar ikke hensyn til reisevei eller kollektivtransport
