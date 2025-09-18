import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def load_sample_bicing(path="data/processed/sample_bicing_stations.csv"):
    df = pd.read_csv(path)
    df['geometry'] = df.apply(lambda r: Point(r.lon, r.lat), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    return gdf

