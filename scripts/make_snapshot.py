# scripts/make_snapshot.py
import os, duckdb

os.makedirs("data/snapshots", exist_ok=True)
out_path = "data/snapshots/snapshot.duckdb"

con = duckdb.connect(out_path)
con.execute("""
  CREATE OR REPLACE TABLE places AS
  SELECT * FROM read_csv_auto('data/seeds/places.csv', header=True)
""")
con.close()
print(f"Snapshot written → {out_path}")