# json_io.py

import os
import json
from models import Book


def save_json(shelf, bookfile="books.json"):
    """Saves books to JSON."""
    data = [book.to_dict() for book in shelf.books]
    with open(bookfile, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_json(shelf, bookfile="books.json"):
    """Uploads books from JSON-file and makes book listing."""
    if not os.path.exists(bookfile):
        print("File not found. Starting an empty bookshelf.")
        return

    with open(bookfile, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            print("File is empty. No books to load.")
            return
        data = json.loads(content)

    shelf.books = [Book.from_dict(item) for item in data]
    print(f"Loaded {len(shelf.books)} books.\n")