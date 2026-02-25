class DogDetector:
    def __init__(self):
        # carregar modelo, pesos, config etc
        pass

    def detect_dog(self, frame) -> bool:
        """
        Retorna True se detectar cachorro no frame
        """
        # ⚠️ placeholder de lógica
        # depois você troca pela detecção real (YOLO, OpenCV, etc)

        if frame is None:
            return False

        # EXEMPLO SIMPLES
        # return True quando detectar cachorro
        return False