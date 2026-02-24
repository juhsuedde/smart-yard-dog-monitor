import cv2
import time

from core.video_source import FileVideoSource, WebcamVideoSource
from detector import DogDetector
from services.telegram_notifier import TelegramNotifier

USE_WEBCAM = False
VIDEO_PATH = "tests/sample.mp4"   # usado se USE_WEBCAM = False
WEBCAM_INDEX = 0

DETECTION_INTERVAL_SECONDS = 10 

def main():
    print("🚀 Iniciando Smart Yard Dog Monitor")

    if USE_WEBCAM:
        video = WebcamVideoSource(index=WEBCAM_INDEX)
        print("📷 Usando webcam")
    else:
        video = FileVideoSource(VIDEO_PATH)
        print(f"🎞️ Usando vídeo: {VIDEO_PATH}")

    video.open()
    print("✅ Fonte de vídeo aberta")

    detector = DogDetector(model_path="yolov8n.pt")
    print("🧠 Detector carregado")

    notifier = TelegramNotifier()
    print("📨 Notificador Telegram pronto")

    last_notification_time = 0

    try:
        while True:
            ret, frame = video.read()

            if not ret or frame is None:
                print("⚠️ Fim do vídeo ou frame inválido")
                break

            detected = detector.detect(frame)

            if detected:
                now = time.time()
                if now - last_notification_time >= DETECTION_INTERVAL_SECONDS:
                    print("🐶 Cachorro detectado! Enviando alerta...")
                    notifier.send_alert(frame=frame)
                    last_notification_time = now

            cv2.imshow("Smart Yard Dog Monitor", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("🛑 Encerrado pelo usuário")
                break

    except KeyboardInterrupt:
        print("🛑 Interrompido pelo usuário")

    finally:
        video.release()
        cv2.destroyAllWindows()
        print("🧹 Recursos liberados. Finalizado.")


if __name__ == "__main__":
    main()