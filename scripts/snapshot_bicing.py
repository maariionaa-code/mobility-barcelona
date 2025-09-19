# scripts/snapshot_bicing.py
import requests, json, time, os
from pathlib import Path
from datetime import datetime
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw" / "bicing"
PROC_DIR = BASE_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

INFO_URL = "https://barcelona-sp.publicbikesystem.net/customer/ube/gbfs/v1/en/station_information"
STATUS_URL = "https://barcelona-sp.publicbikesystem.net/customer/ube/gbfs/v1/en/station_status"

HEADERS = {"User-Agent": "mobility-barcelona/1.0 (+your-email@example.com)"}  # polite

def fetch_json(url, max_retries=3, backoff=2):
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Fetch error (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(backoff * (2 ** attempt))
            else:
                raise

def snapshot():
    now = datetime.utcnow()
    ts = now.strftime("%Y%m%d_%H%M%S")
    fname_json = RAW_DIR / f"bicing_snapshot_{ts}.json"
    fname_parquet = PROC_DIR / f"bicing_snapshot_{ts}.parquet"

    info = fetch_json(INFO_URL).get("data", {}).get("stations", [])
    status = fetch_json(STATUS_URL).get("data", {}).get("stations", [])

    # Normalize
    df_info = pd.json_normalize(info)
    df_status = pd.json_normalize(status)

    # ensure station_id type align
    df_info['station_id'] = df_info['station_id'].astype(str)
    df_status['station_id'] = df_status['station_id'].astype(str)

    # merge
    df = df_info.merge(df_status, on="station_id", how="left", suffixes=("_info","_status"))

    df['snapshot_utc'] = now
    # Save raw JSON (complete) and a compact parquet for analysis
    snapshot_obj = {"fetched_at_utc": now.isoformat(), "info": info, "status": status}
    with open(fname_json, "w", encoding="utf-8") as f:
        json.dump(snapshot_obj, f, ensure_ascii=False)

    # convert columns to friendly names (choose subset)
    cols_keep = [
        "station_id",
        "name",
        "lat",
        "lon",
        "capacity",
        "num_bikes_available",
        "num_bikes_available_types.mechanical",
        "num_bikes_available_types.ebike",
        "num_bikes_disabled",
        "num_docks_available",
        "last_reported",
        "snapshot_utc"
    ]
    # fallback: keep intersection
    keep = [c for c in cols_keep if c in df.columns]
    df[keep].to_parquet(fname_parquet, index=False)

    print("Saved:", fname_json, fname_parquet)
    return fname_json, fname_parquet

if __name__ == "__main__":
    snapshot()
