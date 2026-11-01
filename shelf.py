import textwrap

from models import Book
from ui import UI
from json_io import save_json as _save_json, load_json as _load_json


# -----------------------------
# Bookshelf
# -----------------------------
class Shelf:
    def __init__(self):
        self.books = []


    def _sort_books(self, books=None):

        book_list = self.books if books is None else books
        return sorted(book_list, key=lambda k: (k.year is None, -(k.year or 0), k.title.lower()))

    def _select_book(self, heading="Select a book", sorted_books=None, allow_cancel=True):

        if not self.books:
            print("The shelf is empty.\n")
            return None

        if sorted_books is None:
            sorted_books = self._sort_books()

        UI.clear()
        print(f"\n--- {heading} ---\n")

        for i, book in enumerate(sorted_books, start=1):
            print(f"{i}. {book.default_text()}")

        prompt = "\nNumber"
        if allow_cancel:
            prompt += " (Enter to cancel)"
        prompt += ": "

        user_input = input(prompt).strip()
        if allow_cancel and user_input == "":
            print("Cancelled.\n")
            return None

        try:
            choice = int(user_input)
        except ValueError:
            print("Please enter a number.\n")
            return None

        if choice < 1 or choice > len(sorted_books):
            print("Invalid number.\n")
            return None

        return sorted_books[choice - 1]

    @staticmethod
    def _parse_keywords(text):

        return [s.strip() for s in text.split(",") if s.strip()]



    def add_book(self):
        UI.clear()
        print("\n--- Add a book ---")
        author = input("Author: ")
        title = input("Book title: ")

        keywords_input = input("Enter keywords separated by commas: ")
        keywords = self._parse_keywords(keywords_input)


        while True:
            year_input = input("Publication year (Enter if unknown): ")

            if year_input == "":
                year = None
                break

            try:
                year = int(year_input)
            except ValueError:
                print("Please enter a numeric year.")
                continue

            if not Book.valid_year(year):
                print("Invalid year.")
                continue

            break

        info = input("Additional information (optional): ").strip()

        new_value = Book(author, title, year, info, keywords)
        self.books.append(new_value)
        print("Book added.\n")

    def append_info(self):
        book = self._select_book("Append information")
        if book is None:
            return

        print("\nSelected book:")
        print(book)
        print(f"\nCurrent information:\n{book.info!r}")

        new_value = input("\nEnter text to append: ").strip()
        if not new_value:
            print("Information unchanged.\n")
            return


        if book.info and not book.info.endswith(" "):
            book.info += " "
        book.info += new_value

        print("Information updated.\n")

    def replace_info(self):
        book = self._select_book("Replace information")
        if book is None:
            return

        print("\nSelected book:")
        print(book)
        print(f"\nCurrent information: {book.info!r}")
        print("Press Enter to keep the current information.")

        new_value = input("Enter new information (replaces the current text): ").strip()
        if not new_value:
            print("Information unchanged.\n")
            return

        book.info = new_value
        print("Information replaced.\n")

    def add_keywords(self):
        book = self._select_book("Add keywords")
        if book is None:
            return

        print("\nSelected book:")
        print(book)
        print(f"\nCurrent keywords: {book.keywords!r}\n")
        print("Press Enter to keep the current keywords.")

        new_value = input("Enter keywords to add, separated by commas: ").strip()
        if not new_value:
            print("Keywords unchanged.\n")
            return

        book.keywords.extend(self._parse_keywords(new_value))
        print("Keywords added.\n")

    def delete_book(self):
        book = self._select_book("Delete a book")
        if book is None:
            return

        confirmation = input(f"Delete '{book.title}'? (y/n): ").strip().lower()
        if confirmation != "y":
            print("Deletion cancelled.\n")
            return

        self.books.remove(book)
        print("Book deleted.\n")



    def list_books(self):
        UI.clear()
        print("\n--- Books on shelf ---\n")

        if not self.books:
            print("The shelf is empty.\n")
            return

        sorted_books = self._sort_books()


        for i, book in enumerate(sorted_books, start=1):
            text = book.default_text()
            indented_text = textwrap.indent(text, "    ")
            print(f"{i}.{indented_text}")

    def list_keywords(self):
        UI.clear()
        print("\n--- All keywords ---\n")

        if not self.books:
            print("The shelf is empty.\n")
            return

        all_keywords = set()
        for book in self.books:
            for keyword in book.keywords:
                all_keywords.add(keyword)

        if not all_keywords:
            print("No keywords have been saved.\n")
            return

        for keyword in sorted(all_keywords, key=str.lower):
            print(f"- {keyword}")
        print()

    def search_by_title(self):
        UI.clear()
        print("\n--- Book search ---")
        query = input("Search by title or part of a title: ").strip()
        if not query:
            print("No search term entered.\n")
            return

        normalized_query = query.lower()
        matches = [k for k in self.books if normalized_query in k.title.lower()]

        if not matches:
            print("No books found.\n")
            return


        sorted_matches = self._sort_books(matches)
        UI.clear()
        print("\nSearch results:\n")
        for i, match in enumerate(sorted_matches, start=1):
            book_text = str(match)  # __str__ -> info mukaan
            indented_text = textwrap.indent(book_text, "    ")
            print(f"[{i}]{indented_text}\n")

    def search_by_keyword(self):
        UI.clear()
        print("\n--- Keyword search ---")

        while True:
            query = input("Search by keyword (one word): ").strip()
            if not query:
                print("No search term entered.\n")
                return


            if " " in query or "," in query:
                print("Enter one keyword without spaces or commas.\n")
                continue

            search_term = query.lower()
            matches = []
            for book in self.books:
                if any(search_term in keyword.lower() for keyword in book.keywords):
                    matches.append(book)

            if not matches:
                print("No books found.\n")
                return

            sorted_matches = self._sort_books(matches)
            UI.clear()
            print("\nSearch results:\n")
            for i, match in enumerate(sorted_matches, start=1):
                book_text = str(match)  # info mukaan
                indented_text = textwrap.indent(book_text, "    ")
                print(f"[{i}]{indented_text}\n")
            return

    def search_by_author(self):
        UI.clear()
        print("\n--- Author search ---")
        author_query = input("Search by author or part of a name: ").strip()
        if not author_query:
            print("No search term entered.\n")
            return

        search_term = author_query.lower()
        matches = [k for k in self.books if search_term in k.author.lower()]

        if not matches:
            print("No books found.\n")
            return

        sorted_matches = self._sort_books(matches)
        UI.clear()
        print("\nSearch results:\n")
        for i, found_book in enumerate(sorted_matches, start=1):
            book_text = str(found_book)
            indented_text = textwrap.indent(book_text, "    ")
            print(f"[{i}]{indented_text}\n")

    # json
    def save_json(self, filename="books.json"):
        _save_json(self, filename)

    def load_json(self, filename="books.json"):
        _load_json(self, filename)

    @classmethod
    def load_from_file(cls, filename="books.json"):
        shelf = cls()
        shelf.load_json(filename)
        return shelf

    # ====== Menus ======

    def count(self):
        return len(self.books)

    def main_menu(self):
        UI.clear()
        print("\n=== LIBRARY ===")
        print(f"Books on shelf: {self.count()}")
        print("\n--- Main menu ---")
        print("1. Books")
        print("2. Manage collection")
        print("0. Exit\n")
        return input("Choose an option: ").strip()

    def books_menu(self):
        while True:
            UI.clear()
            print("\n--- Books menu ---")
            print("1. List all books")
            print("2. Search by title / view details")
            print("3. Search by author")
            print("4. Search by keyword")
            print("5. List keywords")
            print("0. Return to main menu\n")

            choice = input("Choose an option: ").strip()

            match choice:
                case "1":
                    self.list_books()
                    input("\nPress Enter to continue...")
                case "2":
                    self.search_by_title()
                    input("\nPress Enter to continue...")
                case "3":
                    self.search_by_author()
                    input("\nPress Enter to continue...")
                case "4":
                    self.search_by_keyword()
                    input("\nPress Enter to continue...")
                case "5":
                    self.list_keywords()
                    input("\nPress Enter to continue...")
                case "0":
                    return
                case _:
                    print("Invalid choice.\n")
                    input("Press Enter to continue...")

    def manage_collection_menu(self):
        while True:
            UI.clear()
            print("\n--- Manage collection ---")
            print("1. Add a book")
            print("2. Append information")
            print("3. Replace information")
            print("4. Add keywords")
            print("5. Delete a book")
            print("0. Return to main menu\n")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_book()
                input("Press Enter to continue...")
            elif choice == "2":
                self.append_info()
                input("Press Enter to continue...")
            elif choice == "3":
                self.replace_info()
                input("Press Enter to continue...")
            elif choice == "4":
                self.add_keywords()
                input("Press Enter to continue...")
            elif choice == "5":
                self.delete_book()
                input("Press Enter to continue...")
            elif choice == "0":
                break
            else:
                print("Invalid choice.\n")
                input("Press Enter to continue...")

    def run(self):
        while True:
            choice = self.main_menu()

            if choice == "1":
                self.books_menu()
            elif choice == "2":
                self.manage_collection_menu()
            elif choice == "0":
                print("Exiting the application.")
                break
            else:
                print("Invalid choice.\n")
                input("Press Enter to continue...")