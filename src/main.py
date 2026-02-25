import cv2

from src.video.video_source import FileVideoSource
from src.detection.dog_detector import DogDetector
from src.notification.telegram_notifier import TelegramNotifier
from src.detection.roi import ROI


def main():
    print("🚀 Iniciando Smart Yard Dog Monitor")

    video_path = "tests/sample.mp4"
    print(f"🎞️ Usando vídeo: {video_path}")

    # Fonte de vídeo
    video = FileVideoSource(video_path)
    video.open()
    print("✅ Fonte de vídeo aberta")

    # ROI (opção B – fixa)
    roi = ROI(x=200, y=150, w=800, h=400)
    print("📐 ROI configurada")

    # Detector
    detector = DogDetector()
    print("🧠 Detector carregado")

    # Notificador
    notifier = TelegramNotifier()
    print("📨 Notificador Telegram pronto")

    try:
        while True:
            ret, frame = video.read()

            if not ret or frame is None:
                print("⚠️ Fim do vídeo ou frame inválido")
                break

            # Aplica ROI
            frame_roi = roi.apply(frame)

            # Detecção
            detected = detector.detect(frame_roi)

            if detected:
                print("🐶 Cachorro detectado! Enviando alerta...")
                notifier.send("🐶 Cachorro detectado no quintal!")
                break  # evita spam em vídeo de teste

            # (opcional) visualizar
            cv2.imshow("Smart Yard Monitor", frame_roi)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        video.release()
        cv2.destroyAllWindows()
        print("🧹 Recursos liberados. Finalizado.")


if __name__ == "__main__":
    main()