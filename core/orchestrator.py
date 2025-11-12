from core.intent import parse_intent
from core.rank import rank_candidates
from core.explain import explain

def run_snapshot_query(user_input: str):
    # Step 1. Parse user query into structured intent
    intent = parse_intent(user_input)

    # Step 2. Rank candidates (initial filtering + scoring)
    results = rank_candidates(intent)

    # Step 3. Generate friendly explanations for each result
    if results and callable(explain):
        for r in results:
            try:
                r["reason"] = explain(intent, r)
            except Exception as e:
                r["reason"] = "Couldn't generate explanation."
                print(f"⚠️ Explain step failed for {r.get('name')}: {e}")

    return intent, results