"""
Downloads plain-text from Project Gutenberg and cleans it up.
Author: Vasilisa Zaitseva.
Date: 2025-05-16
"""

import requests

def fetch_text(url: str) -> str:
    """
    Download the raw text at a PG URL.
    Raises HTTPError if status != 200.
    """
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text

def extract_title(raw_text: str) -> str:
    """
    Heuristic: grab the line after 'Title:' in the header.
    """
    for line in raw_text.splitlines():
        if line.startswith("Title:"):
            return line.replace("Title:", "").strip()
    return "Unknown Title"
