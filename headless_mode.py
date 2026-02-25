#!/usr/bin/env python3
"""
Exemplo avançado: Modo "Headless" (sem interface gráfica)
Útil para rodar em servidor/Raspberry Pi
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.video.video_source import FileVideoSource, WebcamVideoSource
from src.detection.dog_detector import DogDetector
from src.detection.roi import ROI
from src.notification.telegram_notifier import TelegramNotifier
from datetime import datetime, timedelta
import time
import cv2

class HeadlessMonitor:
    """Versão sem GUI para rodar em background."""
    
    def __init__(self, video_source="0", save_detections=True):
        self.video_source_type = video_source
        self.save_detections = save_detections
        self.detection_dir = "detections"
        
        if save_detections and not os.path.exists(self.detection_dir):
            os.makedirs(self.detection_dir)
    
    def run(self):
        """Loop principal sem interface gráfica."""
        print("🤖 Modo Headless iniciado")
        
        # Setup
        if self.video_source_type.isdigit():
            video = WebcamVideoSource(int(self.video_source_type))
        else:
            video = FileVideoSource(self.video_source_type)
        
        if not video.open():
            print("❌ Erro ao abrir vídeo")
            return
        
        roi = ROI()
        detector = DogDetector()
        notifier = TelegramNotifier()
        
        last_alert = None
        cooldown = timedelta(minutes=5)
        frame_count = 0
        
        print(f"📹 Monitorando... (ROI: {roi})")
        print("Pressione Ctrl+C para parar\n")
        
        try:
            while True:
                ret, frame = video.read()
                if not ret:
                    time.sleep(0.1)
                    continue
                
                frame_count += 1
                
                # Processa a cada 5 frames (economiza CPU)
                if frame_count % 5 != 0:
                    continue
                
                # Aplica ROI e detecta
                roi_frame = roi.apply(frame)
                detected = detector.detect(roi_frame)
                
                if detected:
                    now = datetime.now()
                    
                    # Verifica cooldown
                    if last_alert is None or (now - last_alert) >= cooldown:
                        print(f"🐶 [{now.strftime('%H:%M:%S')}] Detecção!")
                        
                        # Salva imagem localmente
                        if self.save_detections:
                            filename = f"{self.detection_dir}/dog_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
                            cv2.imwrite(filename, frame)
                            print(f"   💾 Salvo: {filename}")
                        
                        # Envia para Telegram
                        success = notifier.send_detection_alert(roi_frame)
                        if success:
                            last_alert = now
                            print("   📨 Alerta enviado")
                        else:
                            print("   ⚠️  Falha no envio")
                    else:
                        time_left = cooldown - (now - last_alert)
                        print(f"   ⏱️  Cooldown: {time_left.seconds//60}min restantes")
                
        except KeyboardInterrupt:
            print("\n👋 Encerrando...")
        finally:
            video.release()
            print(f"✅ Total de frames processados: {frame_count}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="0", help="0=webcam ou path do vídeo")
    parser.add_argument("--no-save", action="store_true", help="Não salvar imagens localmente")
    args = parser.parse_args()
    
    monitor = HeadlessMonitor(args.source, save_detections=not args.no_save)
    monitor.run()
