import cv2
import json
import os
from typing import Tuple, Optional

class ROI:
    """Região de Interesse com persistência em arquivo."""
    
    def __init__(self, x: int = 200, y: int = 150, w: int = 800, h: int = 400, config_file: str = "roi.json"):
        self.config_file = config_file
        
        # Tenta carregar do arquivo, senão usa valores padrão
        if os.path.exists(config_file):
            self.load_from_file()
        else:
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.save_to_file()
    
    def apply(self, frame):
        """Aplica ROI no frame e retorna a região cortada."""
        h_frame, w_frame = frame.shape[:2]
        
        # Garante que ROI está dentro dos limites do frame
        x1 = max(0, self.x)
        y1 = max(0, self.y)
        x2 = min(w_frame, self.x + self.w)
        y2 = min(h_frame, self.y + self.h)
        
        return frame[y1:y2, x1:x2]
    
    def draw_on_frame(self, frame, color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 2):
        """Desenha o retângulo da ROI no frame original."""
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), color, thickness)
        cv2.putText(frame, "ROI", (self.x, self.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        return frame
    
    def save_to_file(self):
        """Salva coordenadas da ROI em arquivo JSON."""
        data = {"x": self.x, "y": self.y, "w": self.w, "h": self.h}
        with open(self.config_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 ROI salva em {self.config_file}: {data}")
    
    def load_from_file(self):
        """Carrega coordenadas da ROI do arquivo JSON."""
        with open(self.config_file, "r") as f:
            data = json.load(f)
        self.x = data.get("x", 200)
        self.y = data.get("y", 150)
        self.w = data.get("w", 800)
        self.h = data.get("h", 400)
        print(f"📂 ROI carregada de {self.config_file}: {data}")
    
    def update(self, x: int, y: int, w: int, h: int):
        """Atualiza coordenadas e salva."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.save_to_file()
    
    def is_point_inside(self, px: int, py: int) -> bool:
        """Verifica se um ponto está dentro da ROI."""
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h
    
    def __repr__(self):
        return f"ROI(x={self.x}, y={self.y}, w={self.w}, h={self.h})"
