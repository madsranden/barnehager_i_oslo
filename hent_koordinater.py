"""
Script som henter barnehagekoordinater fra Overpass API (OpenStreetMap)
og matcher dem mot barnehagene i datasettet via fuzzy matching.
Resultatet lagres som en parquet-fil slik at dashbordet slipper API-kall.

Kjør dette scriptet på nytt dersom du vil oppdatere koordinatdataene.
"""

import pandas as pd
import numpy as np
import requests
import re
from rapidfuzz import process

# --- Hent koordinater fra Overpass API ---
query = """
[out:json];
area[name="Oslo"]->.oslo;
nwr[amenity=kindergarten](area.oslo);
out center;
"""

print("Henter barnehagekoordinater fra Overpass API...")
r = requests.post("https://overpass-api.de/api/interpreter", data=query)
elementer = r.json()["elements"]

koord = [
    {
        "navn": e.get("tags", {}).get("name", ""),
        "lat": e.get("lat") or e.get("center", {}).get("lat"),
        "lon": e.get("lon") or e.get("center", {}).get("lon")
    }
    for e in elementer if e.get("tags", {}).get("name")
]

print(f"Fant {len(koord)} barnehager med koordinater i Oslo.")

# --- Fuzzy matching ---
def normaliser(navn, støyende_ord=["barnehage", "as", "avd", "famliebarnehage"]):
    navn = navn.lower()
    for ord in støyende_ord:
        navn = re.sub(rf"\b{ord}\b", "", navn)
    return " ".join(navn.split())


def geocode_fuzzy(navn, koord, terskel=90):
    navn_liste = [normaliser(b["navn"]) for b in koord]
    match, score, idx = process.extractOne(normaliser(navn), navn_liste)
    if score >= terskel:
        return koord[idx]["lat"], koord[idx]["lon"], score, koord[idx]["navn"]
    print(f"  Ingen god match: '{navn}' (beste: '{match}', score: {score:.1f})")
    return None, None, None, None


# Les alle unike barnehager fra datasettet
df = pd.read_parquet("data/barnehager_renset.parquet", engine="fastparquet")
alle_barnehager = df["barnehage"].unique().tolist()

print(f"\nMatcher {len(alle_barnehager)} barnehager fra datasettet...")

df_geo = pd.DataFrame({
    "barnehage": alle_barnehager,
    "Latitude": [np.nan] * len(alle_barnehager),
    "Longitude": [np.nan] * len(alle_barnehager),
    "Match_score": [np.nan] * len(alle_barnehager),
    "Barnehage_fra_api": pd.array([""] * len(alle_barnehager), dtype="string")
})

for idx in df_geo.index:
    lat, lon, score, barnehage_api = geocode_fuzzy(df_geo.iloc[idx, 0], koord)
    df_geo.iloc[idx, 1] = lat
    df_geo.iloc[idx, 2] = lon
    df_geo.iloc[idx, 3] = score
    df_geo.iloc[idx, 4] = barnehage_api

missing = df_geo["Latitude"].isna().sum()
print(f"\nAntall uten match: {missing}")
print(f"Antall matchet: {len(df_geo) - missing}")

# Fjern rader uten koordinater
df_geo = df_geo.dropna(subset=["Latitude"])

# Lagre til parquet
df_geo.to_parquet("data/barnehage_koordinater.parquet", index=False, engine="pyarrow")
print("\nLagret til data/barnehage_koordinater.parquet")
