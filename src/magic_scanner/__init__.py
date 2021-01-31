import argparse
import sys

import pytesseract
import toml
from PySide2.QtWidgets import QApplication

from .main_window import MainWindow
from .tesseract import Tesseract


def toml_file(filename):
    with open(filename, 'r') as fp:
        return toml.load(fp)

def main():
    app = QApplication(sys.argv)

    # Not sure if I should use Qt's argument parsing facilities
    # But I might try and switch this app to tkinter or something
    # and get rid of the Qt dependency
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c',
        default={},
        type=toml_file
    )
    args = parser.parse_args()
    with Tesseract(**args.config.get('tesseract', {})) as tesseract:
        print(f"Tesseract version: {tesseract.version}")
        window = MainWindow(tesseract)

        window.show()

        sys.exit(app.exec_())
