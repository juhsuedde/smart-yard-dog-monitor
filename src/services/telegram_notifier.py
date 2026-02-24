import os
import time
import requests
import cv2
from dotenv import load_dotenv


class TelegramNotifier:
    def __init__(self, cooldown_seconds: int = 300):
        load_dotenv()

        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token or not self.chat_id:
            raise RuntimeError("Variáveis TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não definidas")

        self.cooldown_seconds = cooldown_seconds
        self.last_sent_time = 0

    def send_alert(self, frame=None, message: str = "🐶 Cachorro detectado no quintal!"):
        """
        Envia alerta no Telegram com cooldown.
        Pode enviar texto ou imagem + texto.
        """
        now = time.time()
        if now - self.last_sent_time < self.cooldown_seconds:
            return

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        response = requests.post(url, data=payload)

        if not response.ok:
            print("❌ Falha ao enviar mensagem para o Telegram")
            return

        # Se tiver frame, envia foto também
        if frame is not None:
            self._send_photo(frame, message)

        self.last_sent_time = now

    def _send_photo(self, frame, caption: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

        _, buffer = cv2.imencode(".jpg", frame)

        files = {
            "photo": buffer.tobytes()
        }

        data = {
            "chat_id": self.chat_id,
            "caption": caption
        }

        requests.post(url, data=data, files=files)