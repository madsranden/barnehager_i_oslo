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


#Setter wd
os.chdir("/home/madsranden/Documents/barnehage_analyse")

#Leser data
url = "https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/BHG/FUB/1/3/data"

params = {
    "radSti": "*",
    "filter": (
        "AldergruppeID(-10)_"
        "BarnehageenhetID(-12)_"
        "BarnehageenhetID(-12_4932_9901)_"
        "KjoennID(-10)_"
        "KommunalitetID(-10)_"
        "SpoersmaalID(-122_-64_-63_-62_-59_-58_-57_-55_-54_-53)_"
        "TidID(202601)_"
        "VisAntallBesvart(1)_"
        "VisScore(1)"
    ),
}
#https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/BHG/FUB/1/3/data?radSti=F&filter=AldergruppeID(-10)_BarnehageenhetID(-12_4932_9901)_BarnehagestoerrelsegruppeID(-10)_KjoennID(-10)_KommunalitetID(-10)_SpoersmaalID(-122_-64_-63_-62_-59_-58_-57_-55_-54_-53)_TidID(202601)_VisAntallBesvart(1)_VisScore(1)&dataChanged=2026-02-24_125900


headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, params=params, headers=headers)

response.raise_for_status()  # kaster feil hvis 4xx/5xx

data = response.json()

#Har kommet hit med eksempel-json. Må oppdatere api-kallet og få riktige kolonner fra json-filen.