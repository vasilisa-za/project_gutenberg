"""
Count words and pick the top 10 most common.
Author: Vasilisa Zaitseva.
Date: 2025-05-16
"""

import re
from collections import Counter
from typing import List, Tuple

WORD_RE = re.compile(r"\b[a-zA-Z']{2,}\b")

def top_n_words(text: str, n: int = 10) -> List[Tuple[str,int]]:
    """
    Return the top-n most frequent words (lowercased).
    """
    words = WORD_RE.findall(text.lower())
    counts = Counter(words)
    return counts.most_common(n)
