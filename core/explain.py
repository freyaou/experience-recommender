from utils.llm import run_ollama
from pathlib import Path
import json

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_explain.txt"

def explain(intent: dict, place: dict, model: str = "mistral:instruct") -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    user_input = (
        "intent:\n" + json.dumps(intent, indent=2) +
        "\n\nplace:\n" + json.dumps(place, indent=2)
    )

    return run_ollama(model, system_prompt, user_input)
