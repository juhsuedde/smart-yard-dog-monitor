import cv2
import time


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Não foi possível abrir a fonte de vídeo")
        return

    print("✅ Fonte de vídeo aberta com sucesso")

    last_process_time = 0
    PROCESS_INTERVAL = 1 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Erro ao ler frame")
            break

        now = time.time()

        if now - last_process_time >= PROCESS_INTERVAL:
            last_process_time = now

            print(f"Frame recebido: {frame.shape}")

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()