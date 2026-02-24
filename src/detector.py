from ultralytics import YOLO
import numpy as np


class DogDetector:
    def __init__(self, model_path: str = "yolov8n.pt", confidence_threshold: float = 0.4):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

        self.DOG_CLASS_ID = 16

    def detect(self, frame) -> bool:
        results = self.model(frame, verbose=False)

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                if cls_id == self.DOG_CLASS_ID and conf >= self.confidence_threshold:
                    return True

        return False