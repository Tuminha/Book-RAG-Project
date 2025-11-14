"""
Compose a grounded answer from retrieved chunks with verbatim quotes + citations.

This module defines a *deterministic, reproducible* pipeline that never invents facts.
"""
from typing import List, Dict, Tuple


# === TODO (you code this) ===
# Sentence segmentation utility (pure regex/punctuation-based).
# Hints:
# 1) Split on [.?!] boundaries while keeping punctuation; trim whitespace.
# 2) Discard sentences shorter than a small threshold (e.g., < 20 chars) unless they contain the query's rare terms.
# Acceptance:
# - segment_sentences(text) -> List[str] non-empty for typical chunk.
def segment_sentences(text: str) -> List[str]:
    raise NotImplementedError


# === TODO (you code this) ===
# Scoring function for how well a sentence supports the query.
# Hints:
# 1) Combine simple lexical coverage (overlap of stemmed tokens) + embedding similarity (optional).
# 2) Add brevity penalty (prefer concise quotes) and novelty penalty (deduplicate near-identical sentences).
# 3) Return a float score in [0,1].
# Acceptance:
# - score_sentence(query, sent, sent_vec=None) -> float
def score_sentence(query: str, sentence: str, sent_vec=None) -> float:
    raise NotImplementedError


# === TODO (you code this) ===
# Select top-N quotes from top-k retrieved chunks with diversity.
# Hints:
# 1) For each retrieved item: segment into sentences; score each sentence vs query.
# 2) Rank globally; apply Maximal Marginal Relevance (MMR-lite): skip sentences too close to already-picked ones.
# 3) Attach citation from retrieved.meta (book, chapter/para indices, chunk id).
# Acceptance:
# - select_quotes(query, retrieved, n=3) -> List[Dict{text, score, cite:{...}, chunk_id}]
def select_quotes(query: str, retrieved: List[Dict], n: int = 3) -> List[Dict]:
    raise NotImplementedError


# === TODO (you code this) ===
# Compose a short synthetic answer that *references* selected quotes (no new facts).
# Hints:
# 1) Use a template per intent type: who/what/why/how; detect via first token or heuristics.
# 2) Write 2–4 sentences max; include explicit pointers ("As shown in [1] ...").
# 3) Never assert beyond what the quotes show; avoid absolute claims.
# Acceptance:
# - synthesize_answer(query, quotes) -> str with references like [1], [2], [3]
def synthesize_answer(query: str, quotes: List[Dict]) -> str:
    raise NotImplementedError


# === TODO (you code this) ===
# Render citations block for UI.
# Hints:
# 1) Format: [n] short_snippet — source (book), location (chapter/para or chunk span).
# 2) Shorten long quotes to ~200 chars with ellipses; never alter internal text.
# Acceptance:
# - render_citations(quotes) -> List[str] human-readable lines
def render_citations(quotes: List[Dict]) -> List[str]:
    raise NotImplementedError


# === TODO (you code this) ===
# Main composition entrypoint called by app layer.
# Hints:
# 1) Expect 'retrieved' as list of dicts: {score, text, meta, id}; choose top-N quotes then synthesize answer.
# 2) Return structured payload for UI.
# Acceptance:
# - compose_answer(query, retrieved, max_quotes=3) -> {
#     'answer': str,
#     'quotes': [{'text':str,'score':float,'cite':dict,'chunk_id':str}],
#     'references': ['[1] ...','[2] ...']
#   }
def compose_answer(query: str, retrieved: List[Dict], max_quotes: int = 3) -> Dict:
    raise NotImplementedError

