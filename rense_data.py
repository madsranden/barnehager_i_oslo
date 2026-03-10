# Leser og renser data

#Importerer pakker
import pandas as pd
import numpy as np
import requests
from barnehage_id import hent_barnehage_oslo_id_str

#Lager tekststreng fra barnehage_id.py
barnehage_id = hent_barnehage_oslo_id_str()

#Leser data 
url = f"https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/BHG/FUB/1/3/data\
?radSti=F\
&filter=AldergruppeID(-10)\
_BarnehageenhetID({barnehage_id})\
_BarnehagestoerrelsegruppeID(-10)\
_KjoennID(-10)\
_KommunalitetID(-10)\
_SpoersmaalID(-122_-64_-63_-62_-59_-58_-57_-55_-54_-53)\
_VisAntallBesvart(1)\
_VisScore(1)"

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
antall_barnehager = len(np.unique([i["name"] for i in barnehage_entries])) #Unike barnehager

barnehager = [
    barnehage_entries[i]["name"]
    for i in range(antall_barnehager)
]

#Looper over de forskjellige elementene for å kunne lage en df
list_to_df = []

#Definerer funksjonen som bruker til å håndtere ulike NA
def parse_snitt(verdi):
    if not verdi or verdi.strip() in {"*", ""}:
        return None
    return float(verdi.replace(",", "."))


def parse_antall(verdi):
    if not verdi or verdi.strip() in {"*", ""}:
        return None
    return int(verdi.replace(" ", ""))

for row in rows:
    spørsmål = row["navn"]
    data_values = row["data"]
    
    offset = 0
    barnehage_offset = 0
    
    for år_index, år in enumerate(år_liste):
        
        år_count = år_column_counts[år_index]# Antall verdier til hvert år
        år_slice = data_values[offset:offset + år_count] #slicer de faktiske verdiene
        offset += år_count #Endrer til loop
        antall_barnehager_år = år_count // 2 #Git at vi henter snitt  og antall svar
        # Hent barnehager for dette året
        barnehager_år = barnehage_entries[barnehage_offset : barnehage_offset + antall_barnehager_år]
        barnehage_offset += antall_barnehager_år

        for i, barnehage_dict in enumerate(barnehager_år):
            barnehage = barnehage_dict["name"]
            snitt_idx = i * 2
            antall_idx = snitt_idx + 1
            
            snitt = parse_snitt(år_slice[snitt_idx])
            antall = parse_antall(år_slice[antall_idx])
            
            list_to_df.append({
                "år": år,
                "spørsmål": spørsmål,
                "barnehage": barnehage,
                "snitt": snitt,
                "antall_besvart": antall
            })

df = pd.DataFrame(list_to_df)

#Jukser litt. Hver barnehage skal bare ha 10, 20 eller 30 verdier (spm*år)
filter_verdier = [(i)*len(rows) for i in range(1,len(år_liste)+1)] #Lager liste med mulige verdier

gyldige_barnehager = (
    df.groupby("barnehage")
      .size()
      .loc[lambda x: x.isin(filter_verdier)]
      .index
) #Henter barnehagenavn. 

df_ren = df[df["barnehage"].isin(gyldige_barnehager)]