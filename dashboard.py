import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import distance
from geo_func import avstand_score

st.set_page_config(page_title="Finn den beste barnehagen i Oslo", layout="wide")
st.title("Finn din perfekte barnehage i Oslo", text_alignment = 'center')

#Sidebar-
st.sidebar.header("Innstillinger")

år = st.sidebar.selectbox("År", [2026, 2025, 2023], index=0)

hjem_adresse = st.sidebar.text_input("Hjemadresse", value="Hedmarksgata 4")

vekt_undersokelse = st.sidebar.slider(
    "Vekting av foreldreundersøkelsen",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="0 = kun avstand, 1 = kun foreldreundersøkelsen"
)

# Last data
@st.cache_data
def last_data(år):
    df = pd.read_parquet("data/barnehager_renset.parquet", engine="fastparquet")
    df = df.loc[df["år"] == år, :]

    df_wide = df.pivot_table(
        index=["år", "barnehage", "Eierform"],
        columns="spørsmål",
        values="snitt"
    ).reset_index()

    num_cols = (
        df_wide.loc[:, df_wide.columns != "år"]
        .select_dtypes(include="number")
        .columns
    )
    df_wide[num_cols] = df_wide[num_cols].apply(
        lambda row: row.fillna(row.mean()), axis=1
    )
    df_wide["Gjennomsnittlig_score"] = df_wide[num_cols.drop("Tilfredshet")].mean(axis=1)

    return df_wide


@st.cache_data
def last_koordinater():
    return pd.read_parquet("data/barnehage_koordinater.parquet", engine="pyarrow")


@st.cache_data
def geocode_adresse(adresse):
    geolocator = Nominatim(user_agent="barnehager_dashboard")
    query = f"{adresse}, Oslo, Norge"
    location = geolocator.geocode(query)
    if location:
        return location.latitude, location.longitude
    return None, None


#  Beregning 
df_wide = last_data(år)
df_geo = last_koordinater()
hjem_lat, hjem_lon = geocode_adresse(hjem_adresse)

if hjem_lat is None:
    st.error(f"Kunne ikke finne adressen '{hjem_adresse}'. Prøv en annen adresse.")
    st.stop()

hjem = (hjem_lat, hjem_lon)

# Merge undersøkelse med koordinater
df_merged = pd.merge(df_wide, df_geo[["barnehage", "Latitude", "Longitude"]], on="barnehage", how="left")

# Beregn avstand og score
df_merged = df_merged.dropna(subset=["Latitude"])
df_merged["Avstand_hjem_m"] = df_merged.apply(
    lambda row: distance((row["Latitude"], row["Longitude"]), hjem).m, axis=1
)
df_merged["Avstand_score"] = avstand_score(
    df_merged["Avstand_hjem_m"],
    min=df_wide["Tilfredshet"].min(),
    maks=df_wide["Tilfredshet"].max()
)

vekt_avstand = 1 - vekt_undersokelse
df_merged["Total_score"] = (
    df_merged["Tilfredshet"] * vekt_undersokelse
    + df_merged["Avstand_score"] * vekt_avstand
)

#  Vis resultater 
tab1, tab2 = st.tabs(["Dine topp 15 barnehager", "Kart over barnehager i nærheten"])

# Stolpediagram
with tab1:
    df_top = df_merged.sort_values("Total_score", ascending=False).head(15)
    score_order = df_top.sort_values("Total_score", ascending=False)["barnehage"].tolist()

    fig = px.bar(
        df_top,
        x="Total_score",
        y="barnehage",
        color="Eierform",
        orientation="h",
        range_x=((df_top["Total_score"].min()-1),5),
        labels={"Total_score": "Total score", "barnehage": ""},
        color_discrete_map={"Kommunal": "#4C78A8", "Privat": "#F58518"},
        category_orders={"barnehage": score_order}
    )
    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# Kart
with tab2:
    kart = folium.Map(location=hjem, zoom_start=14)

    for _, row in df_merged.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=row["barnehage"],
            popup=f"{row['barnehage']}<br>Tilfredshet: {row['Tilfredshet']:.2f}<br>Total score: {row['Total_score']:.2f}"
        ).add_to(kart)

    folium.Marker(
        location=hjem,
        tooltip="Hjem",
        popup="Hjem",
        icon=folium.Icon(color="red")
    ).add_to(kart)

    st_folium(kart, use_container_width=True, height=500)

# Sammenleggbar boks (god for lengre tekst)
with open("forklaring_dashbord.md", "r", encoding="utf-8") as f:
    tekst = f.read()

with st.expander("Om dashbordet"):
    st.markdown(tekst)
