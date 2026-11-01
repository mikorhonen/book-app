import os
import subprocess

class UI:
    @staticmethod
    def clear():
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    @staticmethod
    def wait():
        input("\nPress Enter to continue...")
