"""
db.py

Handles SQLite connection, schema creation, and CRUD for books + frequencies.
Author: Vasilisa Z.
Date: 2025-05-16
"""

import sqlite3
from typing import List, Tuple

DB_NAME = "books.db"

def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        title TEXT PRIMARY KEY
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS frequencies (
        title TEXT,
        word TEXT,
        count INTEGER,
        FOREIGN KEY(title) REFERENCES books(title)
    )
    """)
    conn.commit()
    conn.close()

def get_frequencies(title: str) -> List[Tuple[str, int]]:
    """
    Retrieve frequencies for a book whose title contains the input string.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # First, find the closest match for the title
    cur.execute("""
        SELECT title FROM books 
        WHERE LOWER(title) LIKE LOWER(?) 
        LIMIT 1
    """, (f"%{title}%",))
    match = cur.fetchone()

    if not match:
        conn.close()
        return []

    actual_title = match[0]

    # Now fetch the frequencies for the matched title
    cur.execute("""
        SELECT word, count FROM frequencies 
        WHERE title = ? 
        ORDER BY count DESC LIMIT 10
    """, (actual_title,))
    results = cur.fetchall()
    conn.close()
    return results

def save_frequencies(title: str, freqs: List[Tuple[str,int]]):
    """
    Save a new book + its word frequencies into the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO books(title) VALUES(?)", (title,))
    cur.executemany(
        "INSERT INTO frequencies(title, word, count) VALUES (?, ?, ?)",
        [(title, w, c) for w, c in freqs]
    )
    conn.commit()
    conn.close()
