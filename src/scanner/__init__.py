import sys

from PySide2.QtWidgets import QApplication

from .main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec_())
