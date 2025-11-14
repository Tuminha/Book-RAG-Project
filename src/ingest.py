"""
Download public-domain text (Iliad or Dorian Gray) into data/raw/.
"""
from pathlib import Path


def download_book(book: str, out_dir: str) -> str:
    """
    Download the requested book and return local file path.

    # TODO hints:
    # - Use HTTP GET to a stable Project Gutenberg URL for the plain text.
    # - Save as UTF-8 in data/raw/{book}.txt.
    # - Handle re-run: skip if file exists.

    # Acceptance:
    # - Returns a str path to the downloaded file.
    """
    raise NotImplementedError

