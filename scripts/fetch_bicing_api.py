import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

info_url = "https://barcelona-sp.publicbikesystem.net/customer/ube/gbfs/v1/en/station_information"
status_url = "https://barcelona-sp.publicbikesystem.net/customer/ube/gbfs/v1/en/station_status"

def fetch_bicing_data():
    info = requests.get(info_url).json()["data"]["stations"]
    status = requests.get(status_url).json()["data"]["stations"]

    df_info = pd.DataFrame(info)
    df_status = pd.DataFrame(status)

    df = df_info.merge(df_status, on="station_id", suffixes=("_info", "_status"))
    out_path = RAW_DIR / "bicing_realtime.csv"
    df.to_csv(out_path, index=False)
    print(f"✅ Datos guardados en {out_path}")

if __name__ == "__main__":
    fetch_bicing_data()
