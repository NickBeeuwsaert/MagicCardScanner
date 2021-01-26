from PySide2.QtCore import Slot
from PySide2.QtMultimedia import QCameraInfo
from PySide2.QtWidgets import QComboBox


class CameraList(QComboBox):
    def refresh(self):
        self.clear()

        for camera in QCameraInfo.availableCameras():
            self.addItem(camera.description(), camera.deviceName())
