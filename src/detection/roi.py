import cv2
import json
import os
from typing import Tuple

class ROI:
    """Região de Interesse com persistência em arquivo JSON."""
    
    def __init__(self, config_file: str = "roi.json"):
        self.config_file = config_file
        self.load()
    
    def load(self):
        """Carrega coordenadas da ROI do arquivo JSON ou cria padrão."""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
            self.x = data.get("x", 200)
            self.y = data.get("y", 150)
            self.w = data.get("w", 800)
            self.h = data.get("h", 400)
            print(f"📂 ROI carregada: ({self.x}, {self.y}, {self.w}, {self.h})")
        else:
            self.x = 200
            self.y = 150
            self.w = 800
            self.h = 400
            self.save()
            print(f"💾 ROI padrão criada: ({self.x}, {self.y}, {self.w}, {self.h})")
    
    def save(self):
        """Salva coordenadas da ROI em arquivo JSON."""
        data = {"x": self.x, "y": self.y, "w": self.w, "h": self.h}
        with open(self.config_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 ROI salva: {data}")
    
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
    
    def __repr__(self):
        return f"ROI(x={self.x}, y={self.y}, w={self.w}, h={self.h})"