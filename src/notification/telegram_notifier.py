import os
import requests
from typing import Optional
from datetime import datetime
import cv2

class TelegramNotifier:
    """Envia notificações via Telegram (texto e fotos)."""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        if not self.bot_token or not self.chat_id:
            print("⚠️  Variáveis TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configuradas")
        else:
            print("📨 Notificador Telegram inicializado")
    
    def send(self, message: str) -> bool:
        """Envia mensagem de texto."""
        if not self.bot_token or not self.chat_id:
            print("❌ Telegram não configurado. Mensagem não enviada.")
            return False
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Mensagem enviada: {message[:50]}...")
                return True
            else:
                print(f"❌ Erro ao enviar mensagem: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Exceção ao enviar mensagem: {e}")
            return False
    
    def send_photo(self, image_path: str, caption: Optional[str] = None) -> bool:
        """Envia foto para o Telegram."""
        if not self.bot_token or not self.chat_id:
            print("❌ Telegram não configurado. Foto não enviada.")
            return False
        
        if not os.path.exists(image_path):
            print(f"❌ Arquivo não encontrado: {image_path}")
            return False
        
        url = f"{self.base_url}/sendPhoto"
        
        try:
            with open(image_path, "rb") as photo:
                files = {"photo": photo}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption
                    data["parse_mode"] = "HTML"
                
                response = requests.post(url, files=files, data=data, timeout=15)
                
                if response.status_code == 200:
                    print(f"✅ Foto enviada: {image_path}")
                    return True
                else:
                    print(f"❌ Erro ao enviar foto: {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Exceção ao enviar foto: {e}")
            return False
    
    def send_frame(self, frame, caption: Optional[str] = None, temp_path: str = "/tmp/alert_frame.jpg") -> bool:
        """
        Salva frame temporariamente e envia como foto.
        Útil para enviar flagrante do cachorro em tempo real.
        """
        # Salva frame como imagem temporária
        cv2.imwrite(temp_path, frame)
        
        # Adiciona timestamp na legenda
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        full_caption = f"🐶 <b>Cachorro detectado!</b>\n📅 {timestamp}"
        if caption:
            full_caption += f"\n📝 {caption}"
        
        success = self.send_photo(temp_path, full_caption)
        
        # Limpa arquivo temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return success
    
    def send_detection_alert(self, frame, roi_name: str = "quintal") -> bool:
        """Método específico para alerta de detecção com foto."""
        # Adiciona apenas o timestamp no frame, sem banner vermelho
        alert_frame = frame.copy()
        h, w = alert_frame.shape[:2]
        
        # Timestamp discreto no canto inferior
        timestamp = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        cv2.putText(alert_frame, timestamp, (10, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Legenda simples sem emojis estranhos
        caption = f"O cachorro foi detectado na área monitorada."
        
        return self.send_frame(alert_frame, caption)