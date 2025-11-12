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
