
import time

import numpy as np
import pkg_resources
import sqlalchemy
from PySide2.QtCore import Slot
from PySide2.QtGui import QImage
from PySide2.QtMultimedia import QCamera, QVideoProbe
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow

from .decorators import reify
from .image_ops import extract_card, get_image_hash, read_title
from .widgets import CameraList, CameraViewfinder


class MainWindow(QMainWindow):
    camera = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCentralWidget(self.ui)
        self.ui.deviceList.refresh()

        # I can't figure out how to set this in qt designer
        self.ui.splitter.setStretchFactor(0, 3)
        self.ui.splitter.setStretchFactor(1, 1)

        self.setWindowTitle("Magic Card Scanner")
    
    @reify
    def last_frame(self):
        return time.monotonic()

    @reify
    def engine(self):
        return sqlalchemy.engine_from_config(self.config['db'])

    @reify
    def connection(self):
        return self.engine.connect()


    def _on_frame(self, frame):
        now = time.monotonic()
        delta = now - self.last_frame
        if delta < 1/5:
            return
        self.last_frame = now

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
        title = read_title(card)
        phash = get_image_hash(card)
        hash_str = ''.join(format(b, '02x') for b in phash.flat)

        self.ui.cardTitleOCRLineEdit.setText(title)
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
