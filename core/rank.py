import duckdb, json
from pathlib import Path
from utils.llm import run_ollama, extract_json

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_rank.txt"
DB_PATH = Path(__file__).parent.parent / "data" / "snapshots" / "snapshot.duckdb"

def rank_candidates(intent: dict, model: str = "mistral:instruct", limit: int = 50):
    """Ranks candidate places based on how well they match the user's intent."""

    # --- Load system prompt from external file ---
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    # --- Fetch candidate places from DuckDB snapshot ---
    con = duckdb.connect(str(DB_PATH))
    candidates = con.execute("SELECT * FROM places LIMIT ?", [limit]).fetchdf().to_dict(orient="records")
    con.close()

    # --- Construct LLM input ---
    llm_input = f"Intent:\n{json.dumps(intent, indent=2)}\n\nCandidates:\n{json.dumps(candidates, indent=2)}"

    # --- Run LLM to rank candidates ---
    raw = run_ollama(model, system_prompt, llm_input)

    ranked = extract_json(raw)

    # --- Fallback: still return structured output, but no mechanical phrasing ---
    if not ranked:
        print("⚠️ LLM output not valid JSON. Fallback triggered.\nRaw output preview:\n", raw[:400])
        ranked = [{"name": c["name"], "score": 0.5, "reason": ""} for c in candidates]

    return ranked