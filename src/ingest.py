"""
Download public-domain text (Iliad or Dorian Gray) into data/raw/.
"""
from pathlib import Path
import requests


def download_book(book: str, out_dir: str, url: str = None) -> str:
    """
    Download the requested book and return local file path.

    Args:
        book: Book name ('iliad' or 'dorian')
        out_dir: Output directory path (can be relative or absolute)
        url: Optional URL to override default. If None, uses default Project Gutenberg URLs.

    Returns:
        str: Path to the downloaded file.

    # TODO hints:
    # - Use HTTP GET to a stable Project Gutenberg URL for the plain text.
    # - Save as UTF-8 in data/raw/{book}.txt.
    # - Handle re-run: skip if file exists.

    # Acceptance:
    # - Returns a str path to the downloaded file.
    """
    # Map book names to their Project Gutenberg URLs
    book_urls = {
        "iliad": "https://www.gutenberg.org/files/6130/6130-0.txt",
        "dorian": "https://www.gutenberg.org/files/174/174-0.txt"
    }
    
    # Use provided URL or default
    if url is None:
        url = book_urls.get(book)
        if not url:
            raise ValueError(f"Unknown book: {book}. Must be 'iliad' or 'dorian'.")
    
    # Resolve output path (handles relative paths correctly)
    out_path = Path(out_dir).resolve() / f"{book}.txt"
    
    # Skip if file already exists
    if out_path.exists():
        print(f"File already exists: {out_path}")
        return str(out_path)
    
    # Download the book
    print(f"Downloading {book} from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Save to file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(response.text, encoding="utf-8")
    print(f"Saved to: {out_path}")
    
    return str(out_path)
