from abc import ABC, abstractmethod
import cv2
import numpy as np
from typing import Tuple, Optional

class VideoSource(ABC):
    """Classe abstrata para fontes de vídeo."""
    
    @abstractmethod
    def open(self) -> bool:
        """Abre a fonte de vídeo."""
        pass
    
    @abstractmethod
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Lê um frame do vídeo."""
        pass
    
    @abstractmethod
    def release(self):
        """Libera recursos."""
        pass
    
    @abstractmethod
    def is_opened(self) -> bool:
        """Verifica se a fonte está aberta."""
        pass
    
    def set(self, prop_id, value):
        """Define propriedade do vídeo (ex: posição do frame)."""
        pass

class FileVideoSource(VideoSource):
    """Fonte de vídeo a partir de arquivo."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cap = None
    
    def open(self) -> bool:
        self.cap = cv2.VideoCapture(self.file_path)
        if not self.cap.isOpened():
            print(f"❌ Erro ao abrir vídeo: {self.file_path}")
            return False
        print(f"✅ Vídeo aberto: {self.file_path}")
        return True
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if self.cap is None:
            return False, None
        return self.cap.read()
    
    def release(self):
        if self.cap:
            self.cap.release()
            print("🧹 Recursos de vídeo liberados")
    
    def is_opened(self) -> bool:
        return self.cap is not None and self.cap.isOpened()
    
    def set(self, prop_id, value):
        if self.cap:
            self.cap.set(prop_id, value)
    
    def get_fps(self) -> float:
        """Retorna FPS do vídeo."""
        return self.cap.get(cv2.CAP_PROP_FPS) if self.cap else 30.0
    
    def get_total_frames(self) -> int:
        """Retorna número total de frames."""
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) if self.cap else 0

class WebcamVideoSource(VideoSource):
    """Fonte de vídeo a partir de webcam."""
    
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self.cap = None
    
    def open(self) -> bool:
        self.cap = cv2.VideoCapture(self.device_id)
        if not self.cap.isOpened():
            print(f"❌ Erro ao abrir webcam {self.device_id}")
            return False
        print(f"✅ Webcam {self.device_id} aberta")
        return True
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if self.cap is None:
            return False, None
        return self.cap.read()
    
    def release(self):
        if self.cap:
            self.cap.release()
            print("🧹 Webcam liberada")
    
    def is_opened(self) -> bool:
        return self.cap is not None and self.cap.isOpened()

class RTSPVideoSource(VideoSource):
    """Fonte de vídeo a partir de stream RTSP (câmera IP)."""
    
    def __init__(self, rtsp_url: str):
        self.rtsp_url = rtsp_url
        self.cap = None
    
    def open(self) -> bool:
        # Configurações otimizadas para RTSP
        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Buffer pequeno para baixa latência
        
        if not self.cap.isOpened():
            print(f"❌ Erro ao conectar RTSP: {self.rtsp_url}")
            return False
        print(f"✅ Stream RTSP conectado")
        return True
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if self.cap is None:
            return False, None
        return self.cap.read()
    
    def release(self):
        if self.cap:
            self.cap.release()
            print("🧹 Stream RTSP fechado")
    
    def is_opened(self) -> bool:
        return self.cap is not None and self.cap.isOpened()