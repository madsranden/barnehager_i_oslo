#Henter barnehage_ID som tilhører Oslo
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


url = "https://statistikkportalen.udir.no/api/rapportering/rest/v1/Statistikk/BHG/FUB/1/2/filterVerdier"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

response.raise_for_status()  # gir feilmelding hvis 4xx/5xx

data = response.json()