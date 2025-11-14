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
    paragraphs = cleaned.split('\n\n')
    return [p.strip() for p in paragraphs if len(p.strip()) > 0]


def chunk_paragraphs(paragraphs: list, size: int, overlap: int, book: str) -> List[Dict]:
    """
    Make fixed-size chunks with overlap; attach source metadata (book, para_idx, char_span).

    # TODO hints:
    # - Accumulate paragraph text until >= size; slide by size-overlap.
    # - Keep 'source_id' for citations; store start/end character indices.

    # Acceptance:
    # - Returns list of dicts: {id, text, meta:{book, para_idx_start, para_idx_end, span}}
    """
    chunks = []
    chunk_id = 0
    i = 0  # Start from first paragraph
    total_paragraphs = len(paragraphs)
    last_i = -1  # Track last position to detect infinite loops
    
    print(f"📚 Chunking '{book}': {total_paragraphs} paragraphs, size={size}, overlap={overlap}")
    
    while i < len(paragraphs):
        # Safety check: prevent infinite loops
        if i == last_i:
            print(f"⚠️  Warning: Stuck at paragraph {i}, forcing forward progress")
            i += 1
            if i >= len(paragraphs):
                break
        last_i = i
        # Accumulate paragraphs until we reach the target size
        chunk_paras = []
        chunk_text = ""
        para_start_idx = i
        
        # Add paragraphs until we reach or exceed the target size
        while i < len(paragraphs) and len(chunk_text) < size:
            para = paragraphs[i]
            # Add paragraph with separator
            if chunk_text:
                chunk_text += "\n\n" + para
            else:
                chunk_text = para
            chunk_paras.append(i)
            i += 1
        
        # If we have content, create a chunk
        if chunk_text:
            para_end_idx = chunk_paras[-1] if chunk_paras else para_start_idx
            
            chunks.append({
                'id': f'{book}_chunk_{chunk_id}',
                'text': chunk_text,
                'meta': {
                    'book': book,
                    'para_idx_start': para_start_idx,
                    'para_idx_end': para_end_idx,
                    'char_count': len(chunk_text)
                }
            })
            
            # Print progress
            progress_pct = (i / total_paragraphs) * 100
            print(f"  Chunk {chunk_id}: paras {para_start_idx}-{para_end_idx}, {len(chunk_text)} chars ({progress_pct:.1f}% complete)")
            
            chunk_id += 1
            
            # Slide back by (size - overlap) characters for next chunk
            # This creates overlapping chunks
            if i < len(paragraphs) and overlap > 0:
                slide_back = size - overlap
                
                # Find which paragraph to start the next chunk from
                # We want to keep 'overlap' characters from the end of current chunk
                if len(chunk_text) > slide_back:
                    # Work backwards from the end of chunk_text to find where overlap starts
                    # Count characters from the end backwards
                    chars_from_end = 0
                    para_idx_back = len(chunk_paras) - 1
                    
                    # Find the paragraph that contains the start of the overlap region
                    while para_idx_back >= 0:
                        para_idx = chunk_paras[para_idx_back]
                        para_len = len(paragraphs[para_idx])
                        # Add separator length (2 chars for \n\n) if not the last para
                        separator_len = 2 if para_idx_back < len(chunk_paras) - 1 else 0
                        chars_from_end += para_len + separator_len
                        
                        # If we've covered at least 'overlap' chars, we found our starting point
                        if chars_from_end >= overlap:
                            # Start next chunk from this paragraph (included in overlap)
                            next_start_idx = para_idx
                            # CRITICAL: Only move backwards if:
                            # 1. We're going to a different position
                            # 2. It's before the current 'i' (which is already past this chunk)
                            # 3. It's different from where we just were (prevents getting stuck)
                            if next_start_idx < para_end_idx and next_start_idx != last_i:
                                i = next_start_idx
                            else:
                                # Can't safely move backwards, just continue forward from current i
                                # This prevents infinite loops
                                pass
                            break
                        
                        para_idx_back -= 1
                    
                    # Safety check: if we didn't find a good position, just continue forward
                    # This prevents infinite loops
                    if para_idx_back < 0:
                        # Couldn't find overlap point, just continue from where we are
                        # Ensure we at least move forward by 1 paragraph to prevent infinite loops
                        if i <= para_end_idx:
                            i = para_end_idx + 1
                else:
                    # Chunk is smaller than slide_back, can't create meaningful overlap
                    # Just continue from current position
                    pass
        else:
            # No more content
            break
    
    print(f"✅ Created {len(chunks)} chunks from '{book}'")
    return chunks
