import textwrap

class Book:
    def __init__(self, author, title, year, info="", keywords=None):
        self.author = author
        self.title = title
        self.year = year
        self.info = info
        self.keywords = keywords or []  # None -> []

    def __str__(self):
        year = self.year if self.year is not None else "—"
        default = f"{self.author}: {self.title} ({year})"

        if self.info.strip():
            info = textwrap.fill(
                self.info,
                width=80,
                initial_indent="   Info: ",
                subsequent_indent="   "
            )
            return f"{default}\n{info}"

        return default

    def default_text(self):
        year = self.year if self.year is not None else "—"
        return f"{self.author}: {self.title} ({year})"

    def to_dict(self):
        """Creates a dictionary for saving books in JSON."""
        return {
            "author": self.author,
            "title": self.title,
            "year": self.year,
            "info": self.info,
            "keywords": self.keywords
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a book object from dictionary"""
        return cls(
            data["author"],
            data["title"],
            data["year"],
            data.get("info", ""),
            data.get("keywords", [])
        )

    @staticmethod
    def valid_year(year):
        """Rule: The year is accepted only if int and > 0."""
        return isinstance(year, int) and year > 0