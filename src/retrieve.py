"""
Top-k semantic retrieval against FAISS index.
"""
from typing import List, Dict


def retrieve(query: str, index, embed_fn, k: int) -> List[Dict]:
    """
    Return top-k results with text and metadata.

    # TODO hints:
    # - Embed the query; search FAISS for k neighbors; map IDs to metadata rows.

    # Acceptance:
    # - Returns list of dicts: {score, text, meta:{...}} length == k.
    """
    raise NotImplementedError

