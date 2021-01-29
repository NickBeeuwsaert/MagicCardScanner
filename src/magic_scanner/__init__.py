import argparse
import sys

import pytesseract
import toml
from PySide2.QtWidgets import QApplication

from .main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Not sure if I should use Qt's argument parsing facilities
    # But I might try and switch this app to tkinter or something
    # and get rid of the Qt dependency
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tesseract-cmd',
        default=None
    )
    args = parser.parse_args()

    if args.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = args.tesseract_cmd

    window = MainWindow()

    window.show()

    sys.exit(app.exec_())
