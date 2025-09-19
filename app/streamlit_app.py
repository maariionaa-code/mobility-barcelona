import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path

st.set_page_config(page_title="Barcelona Mobility - Demo", layout="wide")
st.title("Barcelona — Urban Mobility (Demo)")

PROC = Path("data") / "processed"
RAW = Path("data") / "raw"
timeseries_path = PROC / "bicing_timeseries.parquet"
realtime_csv = RAW / "bicing_realtime.csv"
sample_path = PROC / "sample_bicing_stations.csv"

# Elegir la fuente de datos disponible
if timeseries_path.exists():
    df_ts = pd.read_parquet(timeseries_path)
    # Tomar el último snapshot de cada estación
    latest = df_ts.sort_values("snapshot_utc").groupby("station_id").tail(1)
    df = latest
elif realtime_csv.exists():
    df = pd.read_csv(realtime_csv)
elif sample_path.exists():
    df = pd.read_csv(sample_path)
else:
    st.error("No data found. Run snapshot_bicing.py or add sample_bicing_stations.csv")
    st.stop()

st.sidebar.write("Fuente de datos usada:")
st.sidebar.write(
    "Timeseries" if timeseries_path.exists()
    else ("Realtime CSV" if realtime_csv.exists() else "Sample CSV")
)

st.metric("Estaciones mostradas", len(df))

st.write("Tabla de estaciones")
st.dataframe(df.head(200))

st.write("Mapa de estaciones")
view = pdk.ViewState(latitude=41.3851, longitude=2.1734, zoom=12)

if 'lon' in df.columns and 'lat' in df.columns:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_radius=60,
        pickable=True
    )
    r = pdk.Deck(layers=[layer], initial_view_state=view)
    st.pydeck_chart(r)
else:
    st.warning("No existen columnas 'lon'/'lat' en los datos")
