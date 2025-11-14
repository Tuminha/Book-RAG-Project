"""
Embeddings + FAISS index build/save/load.
"""
from typing import List, Tuple


def embed_texts(texts: List[str], model_name: str):
    """
    Return matrix of embeddings for texts.

    # TODO hints:
    # - Load SentenceTransformer by name; encode with normalize_embeddings=True if available.
    # - Batch encode; return numpy array (n, d).

    # Acceptance:
    # - Returns embeddings and model reference (if needed).
    """
    raise NotImplementedError


def build_faiss_index(embeddings):
    """
    Build a FAISS index and return it.

    # TODO hints:
    # - Use IndexFlatIP or L2; ensure vectors are normalized if using IP.

    # Acceptance:
    # - Returns a FAISS index ready for add/search.
    """
    raise NotImplementedError


def save_index(index, meta_rows, out_dir: str):
    """
    Persist FAISS index + metadata (CSV/Parquet) to data/index/.

    # TODO hints:
    # - Write index to .faiss and metadata to .parquet with chunk IDs and source info.

    # Acceptance:
    # - Files exist in data/index/.
    """
    raise NotImplementedError


def load_index(in_dir: str):
    """
    Load FAISS index + metadata.

    # TODO hints:
    # - Read index and matching metadata frame; sanity-check row counts.

    # Acceptance:
    # - Returns (index, metadata_df).
    """
    raise NotImplementedError

