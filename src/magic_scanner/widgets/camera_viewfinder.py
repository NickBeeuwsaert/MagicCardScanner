from PySide2.QtMultimediaWidgets import QCameraViewfinder


class CameraViewfinder(QCameraViewfinder):
    """For some reason just passing QCameraViewfinder to QUiLoader doesnt work"""
    pass
