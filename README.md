# ☕ Experience Recommender (MVP)

Find places and experiences that fit your vibe, budget, and mood — powered by structured intent parsing, ranking, and natural language reasoning.

This Streamlit-based app takes a natural query like:

> “quiet coffee with patio in Santa Monica”

and returns personalized, fact-grounded recommendations with friendly one-sentence explanations.

---

## 🧠 How It Works

The pipeline combines traditional data retrieval with LLM reasoning for grounded and explainable recommendations:

```mermaid
flowchart LR
A[User Query] --> B[Intent Parser]
B --> C[Candidate Ranker]
C --> D[Explanation Generator]
D --> E[Streamlit App UI]

1️⃣ Intent Parsing

Extracts city, category, budget, vibe, and distance radius using an LLM system prompt (prompts/system_intent.txt).

Example:

```json
{
  "city": "Santa Monica",
  "category": "coffee",
  "budget": "$",
  "vibe": ["quiet", "outdoor"],
  "max_miles": 5
}
```

2️⃣ Candidate Ranking

Fetches nearby venues from a DuckDB snapshot (data/snapshots/snapshot.duckdb) and scores each candidate using mistral:instruct based on the parsed intent.
Prompt: prompts/system_rank.txt

Example output:
```json
[
  {"name": "Courtyard Cafe", "score": 0.95, "reason": "Located in Santa Monica and offers outdoor seating."},
  {"name": "Good Coffee", "score": 0.70, "reason": "Quiet vibe and patio seating but outside Santa Monica."}
]
```
3️⃣ Natural-Language Explanation

Each ranked result is passed through a lightweight explanation model (prompts/system_explain.txt) to generate one short, friendly sentence — factual, warm, and natural.

Example:

“The Courtyard Cafe in Santa Monica is perfect for your quiet coffee break with its outdoor setting!”

🧩 System Design
Component	Description
core/intent.py	Parses query into structured JSON
core/rank.py	Ranks venues based on intent match
core/explain.py	Generates short human-readable reasoning
core/orchestrator.py	Runs full pipeline end-to-end
app/Home.py	Streamlit front-end interface
prompts/	Modular system prompts for each model stage
data/snapshots/	DuckDB snapshot of candidate places

💻 Run Locally
1. Clone the repo
```bash
git clone https://github.com/<your-handle>/experience-recommender.git
cd experience-recommender
```
2. Install dependencies

You can use either conda or pip:

```bash
conda create -n recommender python=3.12
conda activate recommender
pip install -r requirements.txt
```
3. Launch the app
```bash
streamlit run app/Home.py
```

Then open the link printed in your terminal (usually http://localhost:8501).

🧠 Model Setup (Ollama)

This app uses Ollama
 locally for LLM inference.

Make sure it’s running:

ollama serve


Then pull the required model:

ollama pull mistral:instruct

🧪 Example Query

Input:

quiet coffee with patio in Santa Monica

Output:

🏆 Top Picks

☕ Courtyard Cafe
⭐ Score: 0.95  
The Courtyard Cafe in Santa Monica is perfect for your quiet coffee break with its outdoor setting!

☕ Good Coffee
⭐ Score: 0.70  
Good Coffee in LA has a tranquil vibe and outdoor seating, though it’s not in Santa Monica – maybe a short trip could fit your bill!

☕ Quiet Nook
⭐ Score: 0.35  
Despite being located in Los Angeles, Quiet Nook’s quiet and cozy atmosphere might just make it worth the short drive to Santa Monica for a coffee break.

🧭 Roadmap

 Add memory-based context (e.g., recurring user preferences)

 Extend dataset with Yelp API for live data

 Support multi-turn queries (“somewhere cheaper but still quiet”)

 Evaluate RAG vs fine-tuned LLM ranking layers
