"""
Embeddings + FAISS index build/save/load.
"""
from typing import List
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd


def embed_texts(texts: List[str], model_name: str):
    """
    Return matrix of embeddings for texts.

    # TODO hints:
    # - Load SentenceTransformer by name; encode with normalize_embeddings=True if available.
    # - Batch encode; return numpy array (n, d).

    # Acceptance:
    # - Returns embeddings and model reference (if needed).
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    # Ensure numpy array and float32 for FAISS compatibility
    embeddings = np.array(embeddings, dtype=np.float32)
    return embeddings, model


def build_faiss_index(embeddings):
    """
    Build a FAISS index and return it.

    # TODO hints:
    # - Use IndexFlatIP or L2; ensure vectors are normalized if using IP.

    # Acceptance:
    # - Returns a FAISS index ready for add/search.
    """
    # Ensure embeddings are numpy array and float32
    if not isinstance(embeddings, np.ndarray):
        embeddings = np.array(embeddings, dtype=np.float32)
    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype(np.float32)
    
    # Ensure embeddings are normalized for IndexFlatIP (inner product = cosine similarity)
    # Note: embeddings should already be normalized from embed_texts, but double-check
    faiss.normalize_L2(embeddings)
    
    # Create IndexFlatIP (Inner Product) for normalized vectors
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    return index


def save_index(index, meta_rows, out_dir: str):
    """
    Persist FAISS index + metadata (CSV/Parquet) to data/index/.

    Args:
        index: FAISS index to save
        meta_rows: List of dicts or DataFrame with metadata (chunk IDs, source info)
        out_dir: Output directory path

    # TODO hints:
    # - Write index to .faiss and metadata to .parquet with chunk IDs and source info.

    # Acceptance:
    # - Files exist in data/index/.
    """
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Save FAISS index
    index_path = out_path / 'index.faiss'
    faiss.write_index(index, str(index_path))
    
    # Convert meta_rows to DataFrame if it's a list
    if isinstance(meta_rows, list):
        meta_df = pd.DataFrame(meta_rows)
    elif isinstance(meta_rows, pd.DataFrame):
        meta_df = meta_rows
    else:
        raise ValueError("meta_rows must be a list of dicts or a pandas DataFrame")
    
    # Save metadata
    metadata_path = out_path / 'metadata.parquet'
    meta_df.to_parquet(metadata_path, index=False)
    
    print(f"✅ Saved index to: {index_path}")
    print(f"✅ Saved metadata to: {metadata_path}")
    print(f"   Index size: {index.ntotal} vectors")
    print(f"   Metadata rows: {len(meta_df)}")


def load_index(in_dir: str):
    """
    Load FAISS index + metadata.

    Args:
        in_dir: Input directory path containing index.faiss and metadata.parquet

    # TODO hints:
    # - Read index and matching metadata frame; sanity-check row counts.

    # Acceptance:
    # - Returns (index, metadata_df).
    """
    in_path = Path(in_dir)
    
    # Load FAISS index
    index_path = in_path / 'index.faiss'
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")
    index = faiss.read_index(str(index_path))
    
    # Load metadata
    metadata_path = in_path / 'metadata.parquet'
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    meta_df = pd.read_parquet(metadata_path)
    
    # Sanity check: row counts should match
    if index.ntotal != len(meta_df):
        raise ValueError(
            f"Mismatch: index has {index.ntotal} vectors but metadata has {len(meta_df)} rows"
        )
    
    print(f"✅ Loaded index: {index.ntotal} vectors, dimension {index.d}")
    print(f"✅ Loaded metadata: {len(meta_df)} rows")
    
    return index, meta_df