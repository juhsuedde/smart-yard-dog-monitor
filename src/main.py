import cv2
import time
from detector import DogDetector, box_intersects_roi

ROI = (400, 200, 900, 600)
ALERT_COOLDOWN_SECONDS = 5

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Não foi possível abrir a câmera")
        return

    detector = DogDetector()
    last_alert_time = 0

    print("🎥 Monitorando área com cooldown — pressione 'q' para sair")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Falha ao capturar frame")
            break

        current_time = time.time()
        dogs = detector.detect_dogs(frame)

        rx1, ry1, rx2, ry2 = ROI
        cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)
        cv2.putText(
            frame,
            "AREA MONITORADA",
            (rx1, ry1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

        for (x1, y1, x2, y2) in dogs:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                "DOG",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            if box_intersects_roi((x1, y1, x2, y2), ROI):
                cv2.putText(
                    frame,
                    "⚠️ DOG NA AREA!",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                if current_time - last_alert_time >= ALERT_COOLDOWN_SECONDS:
                    print("⚠️ ALERTA: cachorro dentro da área monitorada")
                    last_alert_time = current_time

        cv2.imshow("Smart Yard Dog Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()