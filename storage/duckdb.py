# storage/duckdb.py
import duckdb
from pathlib import Path

DB_PATH = Path("data/snapshots/snapshot.duckdb")

def get_places(limit: int = 50):
    con = duckdb.connect(DB_PATH)
    rows = con.execute("SELECT * FROM places LIMIT ?", [limit]).fetchall()
    cols = [c[0] for c in con.description]
    con.close()
    # Convert to list of dicts for convenience
    return [dict(zip(cols, r)) for r in rows]