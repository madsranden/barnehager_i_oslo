# Leser og renser data

#Importerer pakker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import os
from geopy.geocoders import Nominatim
import time
import folium
from geopy.distance import distance
from scipy.stats import norm
from scipy import stats
from barnehage_id import hent_barnehage_oslo_id_str


#Leser data 
url = "https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/BHG/FUB/1/3/data?radSti=F&filter=AldergruppeID(-10)_BarnehageenhetID(-12_4932_9901)_BarnehagestoerrelsegruppeID(-10)_KjoennID(-10)_KommunalitetID(-10)_SpoersmaalID(-122_-64_-63_-62_-59_-58_-57_-55_-54_-53)_VisAntallBesvart(1)_VisScore(1)&dataChanged=2026-02-24_125900" #Må legge inn string for riktig id

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

response.raise_for_status()  # gir feilmelding hvis 4xx/5xx

data = response.json()

#Gjør om json til en dataframe
metadata = data["metadata"]
rows = data["rows"]

#Hent år og hvor mange kolonner hvert år har
år_entries = metadata["columns"][0] #gir liste med dict med årene
år_liste = [entry["name"] for entry in år_entries] #gir liste med årene
år_column_counts = [entry["columnCount"] for entry in år_entries] #gir liste med antall verdier per år

# ---- Hent barnehager (per år) ----
# columns[4] inneholder barnehager repetert per år
barnehage_entries = metadata["columns"][4] #Gir liste med dict med barnehagene. Ikke unik så (unike barnehager) * (antall år)

# Antall barnehager per år
antall_barnehager = len(barnehage_entries) // len(år_liste) #Unike barnehager

barnehager = [
    barnehage_entries[i]["name"]
    for i in range(antall_barnehager)
]

#Looper over de forskjellige elementene for å kunne lage en df
list_to_df = []

for row in rows:
    spørsmål = row["navn"]
    data_values = row["data"]
    
    offset = 0
    
    for år_index, år in enumerate(år_liste):
        
        år_count = år_column_counts[år_index]# Antall verdier til hvert år
        år_slice = data_values[offset:offset + år_count] #slicer de faktiske verdiene
        offset += år_count #Endrer til loop
        
        for i, barnehage in enumerate(barnehager):
            
            snitt_idx = i * 2
            antall_idx = snitt_idx + 1
            
            snitt = år_slice[snitt_idx]
            antall = år_slice[antall_idx]
            
            snitt = float(snitt.replace(",", ".")) if snitt else None
            antall = int(antall.replace(" ", "")) if antall else None
            list_to_df.append({
                "år": år,
                "spørsmål": spørsmål,
                "barnehage": barnehage,
                "snitt": snitt,
                "antall_besvart": antall
            })

df = pd.DataFrame(list_to_df)