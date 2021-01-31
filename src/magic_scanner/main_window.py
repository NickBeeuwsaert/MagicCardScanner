
import time

import numpy as np
import pkg_resources
from PySide2.QtCore import Slot
from PySide2.QtGui import QImage
from PySide2.QtMultimedia import QCamera, QVideoProbe
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow

from .decorators import reify, throttle
from .image_ops import extract_card, get_image_hash, get_title
from .widgets import CameraList, CameraViewfinder


class MainWindow(QMainWindow):
    camera = None

    def __init__(self, tesseract, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tesseract = tesseract
        self.setCentralWidget(self.ui)
        self.ui.deviceList.refresh()

        # I can't figure out how to set this in qt designer
        self.ui.splitter.setStretchFactor(0, 3)
        self.ui.splitter.setStretchFactor(1, 1)

        self.setWindowTitle("Magic Card Scanner")

        self.ui.deviceList.activated.connect(lambda _: self.camera_change())

    # run only on a few frames per second so my laptop doesn't melt
    @throttle(1 / 10)
    def _on_frame(self, frame):
        image = frame.image()
        image.convertTo(QImage.Format_BGR888)
        buffer = np.asarray(
            image.bits(),
            dtype=np.uint8
        ).reshape((
            image.height(),
            image.width(),
            3 # 3 color channels (R, G, B)
        ))

        card = extract_card(buffer)
        if card is None:
            return

        title_image = get_title(card)
        if title_image is not None:
            self.tesseract.set_image(title_image)
            self.ui.cardTitleOCRLineEdit.setText(self.tesseract.get_text())

        # My plan for using phashes was that once a card has been manually verified
        # I could pull a high resolution scan of it down from a service like scryfall
        # and phash that, that way next time the same card is scanned we can also 
        # check against the phash of a good scan for better confirmation
        # unfortunately, my webcam is not high enough quality, and doesnt produce a close match
        # to a high resolution scan
        phash = get_image_hash(card)
        hash_str = ''.join(format(b, '02x') for b in phash.flat)
        self.ui.perceptualHashLineEdit.setText(hash_str)


    @Slot()
    def camera_change(self):
        device = self.ui.deviceList.currentData()

        if self.camera:
            self.camera.stop()

        camera = QCamera(bytearray(device, 'utf-8'), self)
        camera.setCaptureMode(
            QCamera.CaptureMode.CaptureViewfinder
        )
        camera.setViewfinder(self.ui.viewfinder)
        self.video_probe.setSource(camera)
        self.camera = camera
        camera.start()

    @reify
    def video_probe(self):
        probe = QVideoProbe(self)
        probe.videoFrameProbed.connect(self._on_frame)
        return probe

    @reify
    def ui(self):
        ui_filename = pkg_resources.resource_filename(__name__, "ui/main.ui")
        
        loader = QUiLoader(self)
        loader.registerCustomWidget(CameraViewfinder)
        loader.registerCustomWidget(CameraList)
        
        return loader.load(ui_filename, self)

    def show(self):
        super().show()
        self.camera_change()
