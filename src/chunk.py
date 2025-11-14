"""
Paragraphization and fixed-size character chunking with overlap.
"""
from typing import List, Dict


def split_into_paragraphs(cleaned: str) -> list:
    """
    Split cleaned text into paragraphs.

    # TODO hints:
    # - Split on double newlines; strip; drop very short fragments.

    # Acceptance:
    # - Returns a list of paragraph strings.
    """
    raise NotImplementedError


def chunk_paragraphs(paragraphs: list, size: int, overlap: int) -> List[Dict]:
    """
    Make fixed-size chunks with overlap; attach source metadata (book, para_idx, char_span).

    # TODO hints:
    # - Accumulate paragraph text until >= size; slide by size-overlap.
    # - Keep 'source_id' for citations; store start/end character indices.

    # Acceptance:
    # - Returns list of dicts: {id, text, meta:{book, para_idx_start, para_idx_end, span}}
    """
    raise NotImplementedError

