import streamlit as st
import os
import duckdb
import pandas as pd

st.title("Experience Recommender (MVP)")
mode = st.radio("Mode", ["Snapshot", "Live (coming soon)"])
prompt = st.text_input("What are you looking for? (e.g., quiet coffee with patio in Santa Monica)")

if st.button("Search") or prompt:
    st.write("Top picks:")
    snap_path = "data/snapshots/snapshot.duckdb"
    if mode == "Snapshot" and os.path.exists(snap_path):
        with duckdb.connect(snap_path, read_only=True) as con:
            df = con.execute("""
                SELECT name, city, price, rating, outdoor
                FROM places
                ORDER BY rating DESC NULLS LAST
                LIMIT 3
            """).fetch_df()
        if len(df) == 0:
            st.info("Snapshot loaded but table is empty—add rows to seeds and rebuild.")
        else:
            for _, row in df.iterrows():
                with st.container(border=True):
                    st.subheader(str(row["name"]))
                    chips = []
                    if not pd.isna(row["rating"]): chips.append(f"⭐ {row['rating']}")
                    if not pd.isna(row["price"]): chips.append("$" * int(row["price"]))
                    if bool(row.get("outdoor", False)): chips.append("patio")
                    st.caption(" • ".join(chips) + f" • {row['city']}")
                    with st.expander("Why this"):
                        st.write("From snapshot demo. Ranking/logics will improve as we build.")
    else:
        # simple mocked cards so UI works even without snapshot
        for i in range(1,4):
            with st.container(border=True):
                st.subheader(f"Mock Place #{i}")
                st.caption("2.1 miles • $$ • patio • quieter • open until 7pm")
                with st.expander("Why this"):
                    st.write("Matches ‘quiet, outdoor, late afternoon’ and is nearby.")