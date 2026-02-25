import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.token or not self.chat_id:
            raise RuntimeError("Token ou Chat ID do Telegram não configurados")

        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send(self, message: str):
        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erro ao enviar mensagem para o Telegram: {response.text}"
            )