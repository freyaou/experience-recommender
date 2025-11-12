# utils/llm.py
import subprocess, json, re

def _ollama_cmd(model: str):
    # just run the model name directly
    return ["ollama", "run", model]

def run_ollama(model: str, system_prompt: str, user_input: str, timeout: int = 60) -> str:
    """
    Runs an Ollama model locally and safely captures all output,
    terminating once generation finishes.
    """
    full_prompt = f"{system_prompt.strip()}\n\nUSER INPUT:\n{user_input.strip()}"

    try:
        # simpler blocking call that guarantees full stdout read
        process = subprocess.run(
            ["ollama", "run", model],
            input=full_prompt,
            text=True,
            capture_output=True,
            timeout=timeout
        )

        if process.returncode != 0:
            print("⚠️ Ollama error:", process.stderr.strip())

        return process.stdout.strip()

    except subprocess.TimeoutExpired:
        print("⚠️ Ollama timed out — returning empty output.")
        return ""

def extract_json(text: str):
    """
    Extracts and parses JSON from a possibly noisy LLM response.
    Finds the first [...]/ {...} block and parses it safely.
    """
    if not text:
        return None

    # Find the first JSON-like block (handles both array or object)
    match = re.search(r'(\[[\s\S]*?\]|\{[\s\S]*?\})', text)
    if not match:
        return None

    json_text = match.group(1)

    # Try direct parsing
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # Try sanitizing: fix single quotes, trailing commas
        fixed = json_text.replace("'", '"')
        fixed = re.sub(r",\s*([\]}])", r"\1", fixed)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            return None