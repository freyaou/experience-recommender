import streamlit as st
import sys, os, json

# --- Path setup ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.orchestrator import run_snapshot_query

# --- Page config ---
st.set_page_config(page_title="Experience Recommender (MVP)", layout="centered")

st.title("🎯 Experience Recommender (MVP)")
st.markdown("Find places and experiences that fit your vibe, budget, and mood.")

# --- Input section ---
query = st.text_input(
    "What are you looking for?",
    placeholder="e.g., quiet coffee shop with patio in Santa Monica",
)

# Initialize
results = None

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        with st.spinner("🔎 Finding your perfect spots..."):
            intent, results = run_snapshot_query(query)

        # Only show results after completion
        if results:
            st.subheader("🏆 Top Picks")
            for r in results:
                if isinstance(r, dict):
                    with st.container():
                        st.markdown(f"### {r['name']}")
                        st.caption(f"⭐ Score: {r.get('score', 'N/A')}")
                        st.write(r.get('reason', 'No explanation available.'))
                        st.divider()
                else:
                    st.write(r)
        else:
            st.info("No matches found or model output was invalid.")