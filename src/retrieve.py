"""
Top-k semantic retrieval against FAISS index.
"""
from typing import List, Dict, Callable
import numpy as np
import faiss


def retrieve(query: str, index, embed_fn: Callable, metadata_df, chunks_lookup: dict = None, k: int = 5) -> List[Dict]:
    """
    Return top-k results with text and metadata.

    Args:
        query: Query string
        index: FAISS index
        embed_fn: Function that takes a string and returns a normalized embedding (numpy array)
        metadata_df: DataFrame with metadata (chunk_id, book, para_idx_start, para_idx_end, char_count)
        chunks_lookup: Optional dict mapping chunk_id to chunk dict with 'text' field
        k: Number of results to return

    Returns:
        List of dicts: {score, text, meta:{...}, chunk_id} length == k.
    """
    # Embed the query using the provided function
    query_embedding = embed_fn(query)
    
    # Ensure query embedding is the right shape and type
    if len(query_embedding.shape) == 1:
        query_embedding = query_embedding.reshape(1, -1)
    if query_embedding.dtype != np.float32:
        query_embedding = query_embedding.astype(np.float32)
    
    # Search FAISS index
    scores, indices = index.search(query_embedding, k)
    
    # Map indices to metadata and return results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(metadata_df):
            continue  # Skip invalid indices
        
        row = metadata_df.iloc[idx]
        chunk_id = row['chunk_id']
        
        # Get text from chunks_lookup if available, otherwise use placeholder
        text = ""
        if chunks_lookup and chunk_id in chunks_lookup:
            text = chunks_lookup[chunk_id].get('text', '')
        elif 'text' in row:
            text = row['text']
        else:
            text = f"[Chunk {chunk_id} - text not available]"
        
        results.append({
            'score': float(score),
            'text': text,
            'chunk_id': chunk_id,
            'meta': {
                'book': row['book'],
                'para_idx_start': int(row['para_idx_start']),
                'para_idx_end': int(row['para_idx_end']),
                'char_count': int(row['char_count'])
            }
        })
    
    return results

