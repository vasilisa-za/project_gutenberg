"""
This module defines the graphical user interface for the Project Gutenberg Explorer.
It allows users to search for book word frequencies either from a local database or by
fetching plain-text files from Project Gutenberg, extracting the top 10 most frequent words.
Author: Vasilisa Zaitseva.
Date: 2025-05-16
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import db, gutenberg, freq

class GutenbergApp:
    """
       A GUI application that allows users to search for and display
       the top 10 most frequent words in books from Project Gutenberg.
    """
    def __init__(self, root):
        """
        Initialize the GUI components, set layout and configure the main window.
        """
        self.root = root
        root.title("📚 Project Gutenberg Explorer")
        root.geometry("700x500")  # Increased size
        root.resizable(True, True)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

        search_frame = ttk.LabelFrame(root, text="🔎 Search Local Database")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Book Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = ttk.Entry(search_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text="Search DB", command=self.search_db).grid(row=0, column=2, padx=5, pady=5)

        fetch_frame = ttk.LabelFrame(root, text="🌐 Fetch from Project Gutenberg")
        fetch_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        fetch_frame.columnconfigure(1, weight=1)

        ttk.Label(fetch_frame, text="Book URL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.url_entry = ttk.Entry(fetch_frame)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(fetch_frame, text="Fetch & Save", command=self.fetch_and_save).grid(row=0, column=2, padx=5, pady=5)

        output_frame = ttk.Frame(root)
        output_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="nsew")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)

        label = ttk.Label(output_frame, text="📊 Top 10 Frequent Words", font=("Segoe UI", 11, "bold"))
        label.grid(row=0, column=0, sticky="w", padx=2, pady=(0, 5))

        self.output = scrolledtext.ScrolledText(output_frame, font=("Courier", 12), wrap=tk.WORD, borderwidth=1,                                        relief="solid")
        self.output.grid(row=1, column=0, sticky="nsew")

        db.init_db()

    def display(self, freqs):
        """
        Display the list of words and their frequencies in the output area.

        Parameters:
        freqs (list of tuple): List of (word, frequency) pairs.
        """
        self.output.delete(1.0, tk.END)
        for word, count in freqs:
            self.output.insert(tk.END, f"{word:<10} {count}\n")

    def search_db(self):
        """
        Retrieve word frequency data for a given book title from the local database
        and display it in the output area.
        """
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Input error", "Please enter a book title.")
            return
        freqs = db.get_frequencies(title)
        if freqs:
            self.display(freqs)
        else:
            messagebox.showinfo("Not found", f"\"{title}\" not in local DB.")

    def fetch_and_save(self):
        """
        Download a book from Project Gutenberg using its plain-text URL,
        extract the top 10 frequent words, save them to the database,
        and display them in the output area.
        """
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input error", "Please enter a URL.")
            return
        try:
            raw = gutenberg.fetch_text(url)
            title = gutenberg.extract_title(raw)
            top = freq.top_n_words(raw, 10)
            db.save_frequencies(title, top)
            self.display(top)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def run_app():
    """
    Entry point for the GUI application.
    """
    root = tk.Tk()
    app = GutenbergApp(root)
    root.mainloop()


