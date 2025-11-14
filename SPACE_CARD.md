# Classics RAG QA — Grounded Q&A for The Iliad and Dorian Gray

**Ask a question → get a concise answer with verbatim quotes and citations.**  

No hallucinations: every claim is backed by text pulled from the book.

---

## ✨ What it does

- Retrieves the most relevant passages from **public-domain editions** (Project Gutenberg).

- Composes a short answer that references **[1][2][3]**-style citations.

- Shows the exact **quoted lines** and where they came from (book, chapter/paragraph).

---

## 🛠️ How it works (under the hood)

1. **Chunk** the cleaned book into overlapping segments with chapter/paragraph metadata.  

2. **Embed** chunks using `sentence-transformers/all-MiniLM-L6-v2`.  

3. **Index** embeddings in FAISS for fast top-k retrieval.  

4. **Compose** answers with a deterministic heuristic:

   - rank candidate sentences by lexical coverage and similarity;

   - select 1–3 diverse quotes;

   - synthesize a 2–4 sentence answer that explicitly references the quotes.

No large language model is required; an optional rewrite step can be added but is **off by default** to preserve groundedness.

---

## 🧪 Evaluation (lightweight)

- **Retrieval Recall@k:** proportion of questions whose gold-support chunk appears in the top-k.  

- **Groundedness:** % of answers with ≥1 quote; **Attribution** = fraction of answer sentences that share ≥2 content words with some quote.  

- On a tiny hand-built QA set (10–20 items), target Recall@5 ≥ 0.8 and Groundedness ≥ 0.95.

> Note: numbers vary by edition and chunking parameters.

---

## 🚀 Try it

- Pick a book (Iliad or Dorian Gray).

- Ask focused questions like:

  - "How does Homer portray Achilles' anger in Book 1?"

  - "What does Lord Henry claim about influence on the young?"

  - "Where does the poem describe the shield of Achilles?"

- Read the answer; expand **Evidence** to inspect quotes and locations.

---

## ⚙️ Configuration

Key parameters (adjusted in `configs/app.yaml`):

- `chunk_size` / `chunk_overlap`: retrieval granularity and recall.

- `embedding_model`: default `all-MiniLM-L6-v2` (speed/quality trade-off).

- `top_k`: number of retrieved chunks shown to the composer.

---

## 📚 Data & Licensing

- Texts are sourced from **Project Gutenberg** (public domain).  

- Only derived chunks and indices are stored for retrieval; we do not redistribute copyrighted editions.

---

## 🔎 Limitations

- Coreference and pronouns may require nearby context; very long-range references can be missed.

- Different translations/editions may shift phrasing and chapter boundaries.

- The system is conservative by design; if quotes are weak, the answer stays cautious.

---

## 🧩 Roadmap

- Named-entity & character graph for richer answers.

- Optional LLM paraphrase pass that **never changes quotes** (off by default).

- Multi-book corpus with per-source filtering and cross-references.

---

## 🧾 Citation

If you reference this project, please cite:

> Classics RAG QA — Grounded Literary Question Answering with Verbatim Citations (2025).  

> https://huggingface.co/spaces/Tuminha/classics-rag-qa

