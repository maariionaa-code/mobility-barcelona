from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"

def load_timeseries(path=None):
    """Carga todo el timeseries parquet de Bicing"""
    if path is None:
        path = PROC / "bicing_timeseries.parquet"
    return pd.read_parquet(path)

def latest_snapshot_gdf(path=None):
    """Devuelve un GeoDataFrame con el último estado de cada estación"""
    df = load_timeseries(path)
    latest = df.sort_values('snapshot_utc').groupby('station_id').tail(1).reset_index(drop=True)
    if 'lon' in latest.columns and 'lat' in latest.columns:
        gdf = gpd.GeoDataFrame(
            latest,
            geometry=[Point(xy) for xy in zip(latest.lon, latest.lat)],
            crs="EPSG:4326"
        )
        return gdf
    else:
        raise ValueError("No se encontraron columnas lon/lat en el dataset")
