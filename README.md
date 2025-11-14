# Classics RAG QA — Grounded Literary Q&A with Verbatim Citations

**What this is**  

A small Retrieval-Augmented Generation (RAG) app for **The Iliad** or **The Picture of Dorian Gray**.  

Ask questions → we retrieve the most relevant passages and produce a concise answer **with verbatim quotes and chapter/line citations**.

**Why it exists**  

- Practice a modern NLP pattern (chunk → embed → index → retrieve → compose).  

- Demonstrate grounded answers with **real citations** (no hand-wavy bot).  

- A pattern you can later swap onto scientific corpora (PubMed, dental abstracts).

---

## Features

- Deterministic ingestion from public-domain sources (Project Gutenberg).  

- Text cleaning: strip front/back matter, normalize whitespace, preserve chapter markers.  

- Flexible chunking (size/overlap configurable).  

- Embeddings via `sentence-transformers` and FAISS index.  

- Gradio demo UI with **quoted evidence** and source refs.

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Work through notebooks in order (01 → 04). Each notebook has TODO cells with hints only.

# After building the index, launch the demo from src/app.py (also TODO scaffold).
```

---

## Project structure

- `notebooks/01_ingest_and_clean.ipynb` – ✅ **Complete** – download & clean text (explain choices).
- `notebooks/02_chunk_and_embed.ipynb` – chunking strategy, embedding preview.
- `notebooks/03_build_index_and_retrieve.ipynb` – FAISS index + retrieval sanity checks.
- `notebooks/04_eval_and_demo.ipynb` – tiny QA set eval + wire the Gradio prototype.
- `src/` modules – minimal signatures & TODOs to turn notebooks into a pipeline.
- `configs/app.yaml` – parameters you can tweak without editing code.

## Progress

- ✅ **Notebook 01**: Ingestion and cleaning complete
  - Implemented `download_book()` with Project Gutenberg integration
  - Implemented `clean_text()` with Gutenberg header/footer removal
  - Both Iliad and Dorian Gray texts successfully downloaded and cleaned

---

## Evaluation (lightweight)

- Build a tiny gold QA set (10–20 Qs).
- Report Recall@k (was a gold answer chunk retrieved?), and a simple groundedness score (% answers with at least one quote).

---

## Data and licensing

Texts from Project Gutenberg (public domain). Do not commit full texts; only derived chunks and indices. See LICENSE.

---

## Roadmap

- Add character/entity index for targeted questions.
- Add optional LLM step to rewrite the composed answer (keeps quotes).
- Package as a Hugging Face Space.

