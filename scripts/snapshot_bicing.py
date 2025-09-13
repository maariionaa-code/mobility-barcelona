#!/usr/bin/env python3
"""
Simple GBFS snapshot saver (Bicing example).
Edit STATION_INFO_URL and STATION_STATUS_URL to the real endpoints.
"""
import os, json, datetime, requests

STATION_INFO_URL = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_show?id=estacions-bicing"  # replace if needed
STATION_STATUS_URL = "https://opendata-ajuntament.barcelona.cat/resource/YOUR_ENDPOINT.json"  # replace with actual endpoint

OUT_DIR = "data/raw/bicing"
os.makedirs(OUT_DIR, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def download(url, filename):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(r.json(), f)

if __name__ == "__main__":
    try:
        # If you don't yet have the real GBFS URLs, this will fail — that's ok for now.
        # You can test the script later once you set the real endpoints.
        download(STATION_INFO_URL, os.path.join(OUT_DIR, f"station_information_{ts}.json"))
        download(STATION_STATUS_URL, os.path.join(OUT_DIR, f"station_status_{ts}.json"))
        print("Snapshots saved to", OUT_DIR)
    except Exception as e:
        print("Snapshot error (expected if endpoints need setup):", e)
