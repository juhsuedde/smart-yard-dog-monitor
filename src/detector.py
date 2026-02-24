from ultralytics import YOLO

class DogDetector:
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect_dogs(self, frame):
        """
        Retorna lista de bounding boxes de cachorros detectados
        Cada box = (x1, y1, x2, y2)
        """
        dogs = []
        results = self.model(frame, verbose=False)

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                if class_name == "dog":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    dogs.append((x1, y1, x2, y2))

        return dogs


def box_intersects_roi(box, roi):
    """
    box = (x1, y1, x2, y2)
    roi = (rx1, ry1, rx2, ry2)
    """
    x1, y1, x2, y2 = box
    rx1, ry1, rx2, ry2 = roi

    return not (
        x2 < rx1 or
        x1 > rx2 or
        y2 < ry1 or
        y1 > ry2
    )