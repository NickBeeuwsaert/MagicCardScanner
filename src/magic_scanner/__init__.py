import argparse
import sys
from tkinter import Tk
from tkinter.ttk import Style

import cv2
import toml

from .tesseract import Tesseract
from .widgets import MainWindow


def toml_file(filename):
    with open(filename, 'r') as fp:
        return toml.load(fp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config', '-c',
        default={},
        type=toml_file
    )
    args = parser.parse_args()
    config = args.config

    root = Tk()
    style = Style(root)
    style.configure("Viewfinder.TFrame", background="black")

    try:
        device_id = config['main']['video_capture_index']
    except KeyError:
        # just use the default camera
        # apparently it is black magic to get the list of camera on a device
        device_id = 0
    capture = cv2.VideoCapture(device_id)

    with Tesseract(**config.get('tesseract', {})) as tesseract:
        main_window = MainWindow(root, capture, tesseract)

        root.mainloop()
