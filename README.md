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
```
---
### 1 Intent Parsing

Extracts city, category, budget, vibe, and distance radius using an LLM system prompt (`prompts/system_intent.txt`).

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
---
### 2 Candidate Ranking

Fetches nearby venues from a DuckDB snapshot (`data/snapshots/snapshot.duckdb`) and scores each candidate using `mistral:instruct` based on the parsed intent.
Prompt: `prompts/system_rank.txt`

Example output:
```json
[
  {"name": "Courtyard Cafe", "score": 0.95, "reason": "Located in Santa Monica and offers outdoor seating."},
  {"name": "Good Coffee", "score": 0.70, "reason": "Quiet vibe and patio seating but outside Santa Monica."}
]
```
### 3 Natural-Language Explanation

Each ranked result is passed through a lightweight explanation model (`prompts/system_explain.txt`) to generate one short, friendly sentence — factual, warm, and natural.

Example:

“The Courtyard Cafe in Santa Monica is perfect for your quiet coffee break with its outdoor setting!”

## 🧩 System Architecture

Below is the current modular design of the Experience Recommender MVP:

```mermaid
flowchart TB
    subgraph User_Interface[🎨 Streamlit Frontend]
        H[app/Home.py]
    end

    subgraph Core_Logic[🧠 Core Logic]
        A[core/intent.py<br>Intent Parser]
        B[core/rank.py<br>Candidate Ranker]
        C[core/explain.py<br>Explanation Generator]
        D[core/orchestrator.py<br>Pipeline Orchestrator]
    end

    subgraph Storage[🗄️ Storage Layer]
        E[storage/duckdb.py<br>Local DuckDB Access]
        F[storage/vectordb.py<br>Vector Database (optional)]
    end

    subgraph Connectors[🔌 External Connectors]
        G[connectors/yelp.py]
        I[connectors/ticketmaster.py]
    end

    subgraph Data_Assets[💾 Data Assets]
        J[data/snapshots/snapshot.duckdb]
        K[data/seeds/places.csv]
    end

    H --> A
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    E --> J
    F --> J
    D --> G
    D --> I
```
---
## 💻 Run Locally
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
---
## 🧠 Model Setup (Ollama)

This app uses Ollama locally for LLM inference.

Make sure it’s running:
```bash
ollama serve
```

Then pull the required model:
```bash
ollama pull mistral:instruct
```
---
## 🚀 Currently Supports

- Natural language query parsing (city, vibe, budget, distance)
- Offline DuckDB snapshot for local venue data
- Local Mistral model inference via Ollama
- Ranking and reasoning through LLM-generated JSON
- Streamlit web UI with interactive search
- Fully modular structure (`core/`, `connectors/`, `storage/`)

---

🔮 Upcoming Features

- Integrate Yelp API for live restaurant & venue data
- Add memory context for recurring user preferences
- Enable multi-turn queries (“find something cheaper nearby”)
- Add filter chips and map visualization in the UI
- Support real-time ranking explanations and confidence scores
- Experiment with RAG-enhanced ranking and lightweight embeddings

## 🧪 Example Query

Input:

quiet coffee with patio in Santa Monica

Output:

🏆 Top Picks

```csharp
☕ Courtyard Cafe
⭐ Score: 0.95  
The Courtyard Cafe in Santa Monica is perfect for your quiet coffee break with its outdoor setting!

☕ Good Coffee
⭐ Score: 0.70  
Good Coffee in LA has a tranquil vibe and outdoor seating, though it’s not in Santa Monica – maybe a short trip could fit your bill!

☕ Quiet Nook
⭐ Score: 0.35  
Despite being located in Los Angeles, Quiet Nook’s quiet and cozy atmosphere might just make it worth the short drive to Santa Monica for a coffee break.
```
