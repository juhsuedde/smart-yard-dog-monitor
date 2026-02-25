from ultralytics import YOLO
import cv2
import numpy as np
from typing import List, Tuple, Optional

class DogDetector:
    """Detector de cães usando YOLOv8."""
    
    # COCO dataset class ID para "dog" é 16
    DOG_CLASS_ID = 16
    CONFIDENCE_THRESHOLD = 0.5
    
    def __init__(self, model_path: str = "yolov8n.pt"):
        """
        Inicializa o detector.
        
        Args:
            model_path: Caminho para o modelo YOLO (baixa automaticamente se não existir)
        """
        try:
            self.model = YOLO(model_path)
            print(f"🧠 Modelo YOLO carregado: {model_path}")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            raise
    
    def detect(self, frame) -> bool:
        """
        Detecta se há cachorro no frame.
        
        Args:
            frame: Imagem em formato BGR (OpenCV)
            
        Returns:
            True se detectou cachorro, False caso contrário
        """
        results = self.model(frame, verbose=False)
        
        for result in results:
            if result.boxes is None:
                continue
                
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                if class_id == self.DOG_CLASS_ID and confidence >= self.CONFIDENCE_THRESHOLD:
                    return True
        
        return False
    
    def detect_with_visualization(self, frame, draw_boxes: bool = True) -> Tuple[bool, np.ndarray]:
        """
        Detecta cachorro e retorna frame com anotações visuais.
        
        Returns:
            Tuple (detected, annotated_frame)
        """
        results = self.model(frame, verbose=False)
        detected = False
        annotated_frame = frame.copy()
        
        for result in results:
            if result.boxes is None:
                continue
                
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                if class_id == self.DOG_CLASS_ID and confidence >= self.CONFIDENCE_THRESHOLD:
                    detected = True
                    
                    if draw_boxes:
                        # Coordenadas da caixa
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        # Desenha caixa vermelha
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        
                        # Label com confiança
                        label = f"Cachorro: {confidence:.2f}"
                        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return detected, annotated_frame
    
    def get_detections(self, frame) -> List[dict]:
        """
        Retorna lista de detecções com coordenadas e confiança.
        
        Returns:
            Lista de dicts: {'bbox': (x1, y1, x2, y2), 'confidence': float}
        """
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            if result.boxes is None:
                continue
                
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                if class_id == self.DOG_CLASS_ID and confidence >= self.CONFIDENCE_THRESHOLD:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append({
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence
                    })
        
        return detections