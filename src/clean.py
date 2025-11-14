"""
Clean raw text: remove Gutenberg headers/footers, normalize whitespace, keep chapter markers.
"""


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
    raise NotImplementedError

