import cv2
from abc import ABC, abstractmethod


class VideoSource(ABC):
    """
    Interface base para qualquer fonte de vídeo:
    - arquivo
    - webcam
    - RTSP (futuro)
    """

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def release(self):
        pass


class FileVideoSource(VideoSource):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.file_path)
        if not self.cap.isOpened():
            raise RuntimeError(f"Não foi possível abrir o vídeo: {self.file_path}")

    def read(self):
        if self.cap is None:
            raise RuntimeError("Fonte de vídeo não foi aberta")
        return self.cap.read()

    def release(self):
        if self.cap:
            self.cap.release()


class WebcamVideoSource(VideoSource):
    def __init__(self, index: int = 0):
        self.index = index
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.index)
        if not self.cap.isOpened():
            raise RuntimeError("Não foi possível acessar a webcam")

    def read(self):
        if self.cap is None:
            raise RuntimeError("Fonte de vídeo não foi aberta")
        return self.cap.read()

    def release(self):
        if self.cap:
            self.cap.release()