"""
Compose a grounded answer from retrieved chunks with verbatim quotes + citations.

This module defines a *deterministic, reproducible* pipeline that never invents facts.
"""
from typing import List, Dict, Tuple
import re


def segment_sentences(text: str) -> List[str]:
    """
    Split text into sentences using punctuation boundaries.
    
    Returns non-empty sentences (minimum 20 chars or contains query terms).
    """
    # Split on sentence boundaries (. ! ?) while keeping punctuation
    sentences = re.split(r'([.!?]+)', text)
    
    # Recombine sentences with their punctuation
    result = []
    for i in range(0, len(sentences) - 1, 2):
        if i + 1 < len(sentences):
            sentence = (sentences[i] + sentences[i + 1]).strip()
        else:
            sentence = sentences[i].strip()
        
        # Keep sentences that are at least 20 chars or contain meaningful content
        if len(sentence) >= 20:
            result.append(sentence)
    
    return result if result else [text]  # Fallback to full text if no sentences found


def score_sentence(query: str, sentence: str, sent_vec=None) -> float:
    """
    Score how well a sentence supports the query.
    
    Simple lexical overlap score (0-1 range).
    """
    # Normalize to lowercase for comparison
    query_lower = query.lower()
    sentence_lower = sentence.lower()
    
    # Split into words (simple tokenization)
    query_words = set(re.findall(r'\b\w+\b', query_lower))
    sentence_words = set(re.findall(r'\b\w+\b', sentence_lower))
    
    if not query_words:
        return 0.0
    
    # Calculate overlap ratio
    overlap = len(query_words & sentence_words)
    coverage = overlap / len(query_words)
    
    # Add brevity bonus (prefer concise sentences)
    brevity_bonus = min(1.0, 100 / len(sentence)) * 0.1
    
    score = min(1.0, coverage + brevity_bonus)
    return score


def select_quotes(query: str, retrieved: List[Dict], n: int = 3) -> List[Dict]:
    """
    Select top-N quotes from retrieved chunks with diversity.
    
    Simple implementation: segment into sentences, score them, pick top-N.
    """
    all_sentences = []
    
    # For each retrieved chunk, segment and score sentences
    for item in retrieved:
        text = item.get('text', '')
        if not text:
            continue
        
        sentences = segment_sentences(text)
        for sent in sentences:
            score = score_sentence(query, sent)
            all_sentences.append({
                'text': sent,
                'score': score,
                'chunk_id': item.get('chunk_id', ''),
                'cite': item.get('meta', {})
            })
    
    # Sort by score and take top-N
    all_sentences.sort(key=lambda x: x['score'], reverse=True)
    
    # Simple diversity: skip sentences that are too similar to already selected ones
    selected = []
    for sent_data in all_sentences:
        if len(selected) >= n:
            break
        
        # Check if too similar to already selected (simple check: same chunk or very similar text)
        is_duplicate = False
        for existing in selected:
            if sent_data['chunk_id'] == existing['chunk_id']:
                # Same chunk - only add if significantly different
                if sent_data['text'][:50] == existing['text'][:50]:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            selected.append(sent_data)
    
    return selected[:n]


def synthesize_answer(query: str, quotes: List[Dict]) -> str:
    """
    Compose a short synthetic answer that references selected quotes.
    
    Simple template-based approach.
    """
    if not quotes:
        return "I couldn't find relevant information to answer this question."
    
    # Detect query type (simple heuristic)
    query_lower = query.lower()
    if query_lower.startswith(('who', 'what', 'where', 'when', 'why', 'how')):
        question_word = query_lower.split()[0]
    else:
        question_word = "what"
    
    # Build answer with references
    answer_parts = []
    
    if question_word == "what":
        answer_parts.append(f"Based on the text, {query_lower.replace('what', '').replace('?', '').strip()}:")
    elif question_word == "who":
        answer_parts.append(f"Regarding {query_lower.replace('who', '').replace('?', '').strip()}:")
    elif question_word == "how":
        answer_parts.append(f"Here's how {query_lower.replace('how', '').replace('?', '').strip()}:")
    else:
        answer_parts.append("Based on the retrieved passages:")
    
    # Add references to quotes
    for i, quote in enumerate(quotes, 1):
        text = quote['text']
        # Truncate long quotes
        if len(text) > 150:
            text = text[:150] + "..."
        answer_parts.append(f"\n\nAs shown in [{i}]: {text}")
    
    return " ".join(answer_parts)


def render_citations(quotes: List[Dict]) -> List[str]:
    """
    Render citations block for UI.
    
    Format: [n] short_snippet — source (book), location (paragraphs).
    """
    citations = []
    for i, quote in enumerate(quotes, 1):
        text = quote['text']
        # Shorten to ~200 chars with ellipses
        if len(text) > 200:
            text = text[:200] + "..."
        
        cite = quote.get('cite', {})
        book = cite.get('book', 'unknown')
        para_start = cite.get('para_idx_start', '?')
        para_end = cite.get('para_idx_end', '?')
        
        citation = f"[{i}] {text} — {book.title()}, paragraphs {para_start}-{para_end}"
        citations.append(citation)
    
    return citations


def compose_answer(query: str, retrieved: List[Dict], max_quotes: int = 3) -> Dict:
    """
    Main composition entrypoint called by app layer.
    
    Returns structured payload for UI.
    """
    if not retrieved:
        return {
            'answer': "I couldn't find any relevant information to answer this question.",
            'quotes': [],
            'references': []
        }
    
    # Select top quotes
    quotes = select_quotes(query, retrieved, n=max_quotes)
    
    # Synthesize answer
    answer = synthesize_answer(query, quotes)
    
    # Render citations
    references = render_citations(quotes)
    
    return {
        'answer': answer,
        'quotes': quotes,
        'references': references
    }

