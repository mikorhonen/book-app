from shelf import Shelf

def main():
    shelf = Shelf.load_from_file()
    shelf.run()
    shelf.save_json()


if __name__ == "__main__":
    main()