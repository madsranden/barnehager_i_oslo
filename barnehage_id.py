#Henter barnehage_ID som tilhører Oslo
#Importerer pakker
import pandas as pd
import numpy as np
import requests
import os

def hent_barnehage_oslo_id_str():
    
    #Api-kall til metadata om strukturen til datasettet
    url = "https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/BHG/FUB/1/2/filterVerdier"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # gir feilmelding hvis 4xx/5xx
    data = response.json()
    
    #Liste med id med alle bydelene
    df = pd.DataFrame(data["BarnehageenhetID"])
    bydels_id = df.loc[df["navn"] == "Oslo", "barn"].iloc[0] #Lager liste med bydels_id
    df_bydeler = df.loc[df['indeks'].isin(bydels_id), :] #Filtrerer basert på listen
    barnehage_id = df_bydeler.loc[:, "barn"].tolist()
    flat_liste = []
    for i in barnehage_id:
        for x in i:
            flat_liste.append(x) #Unnester listen for å bruke den til å filtere
    df_barnehager = df.loc[df['indeks'].isin(flat_liste), :]
    
    #Jeg trenger kun id for å filtrere til api-kalletabs
    barnehager_oslo_id = (
        df_barnehager.loc[:,"id"]
            .astype(str)
            .tolist()
    )
    barnehage_oslo_id_str = "_".join(barnehager_oslo_id) #Api-kallet trenger kun en streng med id-er.
    return barnehage_oslo_id_str