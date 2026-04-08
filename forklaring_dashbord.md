Å velge barnehage til barnet sitt er ikke enkelt. Heldigvis finnes det data som kan gjøre valget mer opplyst.

Rangeringen på denne siden bruker data fra Foreldreundersøkelsen som gjennomføres hvert år av Udir. Dette kombineres med kartdata der barnehager nærmest din hjemadresse får den beste scoren. Resultatet er en rangering av alle barnehagene i Oslo jeg har tilgang på data for. De 15 høyest rangerte barnehagene vises i stolpediagrammet. I kartet kan barnehagene undersøkes nærmere. Hjemadressen er markert med en rød pin. 

Barnehager som ikke har tall fra foreldreundersøkelsen eller mangler kartdata er ikke en del av analysen. Bruk derfor tallene med varsomhet og sjekk Oslo kommunes nettsider for en oppdatert oversikt over aktuelle barnehager. 

### Hvordan bruke dashbordet?
- **År:** Sett året du ønsker tall fra foreldreundersøkelsen. Dette danner den ene delen av grunnlaget for rangeringen i stolpediagrammet. På nåværende tidspunkt er tall fra 2026, 2025 og 2023 tilgjengelig. 
- **Hjemadresse:** Skriv inn adressen du ønsker å bruke. Avstanden fra adressen brukes til å regne ut en poengsum til hver barnehage. 
- **Vekting av foreldreundersøkelsen:** Dette brukes for å justere rangeringen til å passe bedre med din preferanse. Dersom du kun er opptatt av hvilken barnehage som nærmest setter du parameteret til 0. Dersom du kun er opptatt av resultatet fra foreldreundersøkelsen setter du det til 1. 

### Nærmere om tallene og metoden
#### Data: 
- **Foreldreundersøkelsen:** Tilgjengelig fra [Udir](https://www.udir.no/tall-og-forskning/statistikk/statistikk-barnehage/fuba-resultater-alle-sporsmal/). Foreldrene scorer barnehagen på en skala fra 1 til 5 på temaer som tilfredshet, barns medvirkning og lek. 
- **Kartdata:** Hentet fra OpenStreetMap via [Overpass API](https://overpass-api.de/) for geolokasjon av barnehagene. Hjemadresse geokodes ved hjelp av Kartverkets API. Klikk [her](https://ws.geonorge.no/adresser/v1/#/default/get_sok) for mer informasjon og søkehjelp til å finne riktig hjemadresse for deg.

#### Metode
- **Score fra foreldreundersøkelsen:** Variabelen "tilfredshet" er antatt å fange opp foreldrenes helhetsinntrykk av barnehagen. Den gjennomsnittlige poengsummen fra denne variabelen danner grunnlaget for denne scoren. Det har ikke vært mulig å ta hensyn til statistisk usikkerhet, som særlig i små barnehager vil være stor. 
- **Score fra avstand:** Denne poengsummen er gitt ved formelen:  
  
  $f(Avstand) = min(Tilfredshet) + \frac{maks(Tilfredshet)-min(Tilfredshet)}{(1+0.0005Avstand)}$  
  
  Funksjonen sikrer at vi bruker den samme skalen som foreldreundersøkelsen, og er fallende i avstand. Dersom den høyste scoren på tilfredshet er 5 og den laveste er 3,4, vil en barnehage som er én kilometer unna få poengsummen 4,5. En barnehage som er 100 meter unna får 4.9 og en barnehage 10 kilometer unna får 3,7 osv. For særlig interesserte finnes det nærmere forklaring på hvordan jeg bruker denne funksjonen på [Github](https://github.com/madsranden/barnehager_i_oslo). 

**En siste disclaimer:** Dette er i hovedsak et privat hobbyprosjekt laget i pappaperm for å opprettholde noen gamle Python-ferdigheter. Koden og analysen deles åpent i håp om at den kanskje kan være nyttig for andre, men prosjektet vedlikeholdes ikke aktivt. 