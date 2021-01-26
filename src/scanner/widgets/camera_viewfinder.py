from PySide2.QtMultimediaWidgets import QCameraViewfinder


class CameraViewfinder(QCameraViewfinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet("* { background-color: black }")
