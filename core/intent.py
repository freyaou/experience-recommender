import json
from pathlib import Path
from utils.llm import run_ollama

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_intent.txt"

def parse_intent(user_text: str, model: str = "mistral:instruct") -> dict:
    system_prompt = open(PROMPT_PATH).read()
    raw = run_ollama(model, system_prompt, user_text)
    try:
        intent = json.loads(raw)
    except json.JSONDecodeError:
        intent = {"city": "Los Angeles", "category": "restaurant",
                  "budget": "$$", "vibe": [], "max_miles": 5.0}
    intent["raw_prompt"] = user_text
    return intent