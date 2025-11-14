"""
Clean raw text: remove Gutenberg headers/footers, normalize whitespace, keep chapter markers.
"""
import re

def clean_text(raw_path: str) -> str:
    """
    Load raw text and return a cleaned string.

    # TODO hints:
    # - Strip front/back matter by searching for known separators.
    # - Normalize whitespace with regex; keep blank lines between paragraphs.
    # - Preserve CHAPTER markers if present.

    # Acceptance:
    # - Returns a non-empty cleaned string.
    """
    with open(raw_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Find and extract content between Gutenberg markers
    # Pattern matches: *** START OF THE PROJECT GUTENBERG EBOOK [number] ***
    start_pattern = r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK \d+ \*\*\*'
    end_pattern = r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK \d+ \*\*\*'
    
    # Find start marker
    start_match = re.search(start_pattern, text, re.IGNORECASE)
    if start_match:
        # Extract text after the start marker
        text = text[start_match.end():]
    else:
        # Fallback: try alternative patterns
        alt_start = re.search(r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK \*\*\*', text, re.IGNORECASE)
        if alt_start:
            text = text[alt_start.end():]
    
    # Find end marker
    end_match = re.search(end_pattern, text, re.IGNORECASE)
    if end_match:
        # Extract text before the end marker
        text = text[:end_match.start()]
    else:
        # Fallback: try alternative patterns
        alt_end = re.search(r'\*\*\* END OF THIS PROJECT GUTENBERG EBOOK \*\*\*', text, re.IGNORECASE)
        if alt_end:
            text = text[:alt_end.start()]

    # Remove common Gutenberg metadata at the beginning (title, author, table of contents)
    # But keep the actual book content including chapter markers
    lines = text.split('\n')
    cleaned_lines = []
    in_toc = False  # Track if we're in table of contents
    content_started = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines at the very beginning
        if not content_started and not line_stripped:
            continue
            
        # Detect table of contents section
        if not content_started and line_stripped.lower() == 'contents':
            in_toc = True
            continue
        
        # Skip table of contents entries (simple chapter lists)
        if in_toc:
            if re.match(r'^CHAPTER [IVX]+\.?$', line_stripped, re.IGNORECASE):
                continue
            # End of TOC when we hit actual content
            if line_stripped and len(line_stripped) > 20:
                in_toc = False
                content_started = True
            else:
                continue
        
        # Skip simple title/author lines (very short, title-case only)
        if not content_started and line_stripped:
            # Skip if it's a simple title (2-4 words, all title case, no punctuation)
            if re.match(r'^[A-Z][a-z]+( [A-Z][a-z]+){1,3}$', line_stripped) and len(line_stripped) < 50:
                continue
            # Skip "by Author Name" lines
            if re.match(r'^by [A-Z][a-z]+ [A-Z]', line_stripped, re.IGNORECASE):
                continue
            # Once we hit substantial content, start keeping everything
            if len(line_stripped) > 20 or 'CHAPTER' in line_stripped.upper():
                content_started = True
        
        cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)

    # Normalize whitespace: collapse multiple spaces/tabs but preserve newlines (paragraph breaks)
    text = re.sub(r'[ \t]+', ' ', text)  # Collapse spaces/tabs to single space
    text = re.sub(r'[ \t]*\n[ \t]*', '\n', text)  # Normalize line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)  # Collapse 3+ newlines to double newline
    text = text.strip()

    return text
