# scripts/merge_snapshots.py
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"
out = PROC / "bicing_timeseries.parquet"

parquets = sorted(PROC.glob("bicing_snapshot_*.parquet"))
if not parquets:
    print("No parquet snapshots found in", PROC)
    raise SystemExit(0)

dfs = [pd.read_parquet(p) for p in parquets]
df = pd.concat(dfs, ignore_index=True)

# unify column names
if "num_bikes_available_types.mechanical" in df.columns:
    df = df.rename(columns={
        "num_bikes_available_types.mechanical": "ebikes_mechanical",
        "num_bikes_available_types.ebike": "ebikes_ebike"
    })

# cast types
df['snapshot_utc'] = pd.to_datetime(df['snapshot_utc'])
df = df.sort_values(['station_id','snapshot_utc'])

# save a compact timeseries (overwrite)
df.to_parquet(out, index=False)
print("Written aggregated timeseries to", out)

