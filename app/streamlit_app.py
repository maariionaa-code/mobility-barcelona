import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Barcelona Mobility - Demo", layout="wide")
st.title("Barcelona — Urban Mobility (Demo)")

try:
    df = pd.read_csv("data/raw/bicing_realtime.csv")
except Exception as e:
    st.error("Sample data not found. Add data/processed/sample_bicing_stations.csv")
    st.stop()

st.write("Sample Bicing stations")
st.dataframe(df)

st.write("Map (sample)")
view = pdk.ViewState(latitude=41.3851, longitude=2.1734, zoom=12)
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_radius=100,
    get_fill_color=[255, 0, 0],
    pickable=True
)
r = pdk.Deck(layers=[layer], initial_view_state=view)
st.pydeck_chart(r)
