#!/usr/bin/env python3
"""
Smart Yard Dog Monitor v2.1 - ROI via JSON
Configure a ROI editando o arquivo roi.json
"""

import cv2
import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.video.video_source import FileVideoSource, WebcamVideoSource, RTSPVideoSource
from src.detection.dog_detector import DogDetector
from src.detection.roi import ROI
from src.notification.telegram_notifier import TelegramNotifier

load_dotenv()


class SmartYardMonitor:
    """Sistema principal de monitoramento."""
    
    def __init__(self, video_path="tests/sample.mp4"):
        self.video_path = video_path
        self.video_source = None
        self.roi = None
        self.detector = None
        self.notifier = None
        self.last_alert = None
        self.alert_cooldown = timedelta(minutes=5)
        self.frame_count = 0
        self.detection_count = 0
        
    def setup(self):
        print("\n🚀 Smart Yard Dog Monitor v2.1")
        print("=" * 40)
        
        # Fonte de vídeo
        if self.video_path.startswith("rtsp://"):
            self.video_source = RTSPVideoSource(self.video_path)
        elif self.video_path.isdigit():
            self.video_source = WebcamVideoSource(int(self.video_path))
        else:
            self.video_source = FileVideoSource(self.video_path)
        
        if not self.video_source.open():
            raise RuntimeError("Não foi possível abrir vídeo")
        
        # ROI (carrega de roi.json)
        self.roi = ROI()
        print(f"📐 ROI ativa: {self.roi}")
        
        # Componentes
        self.detector = DogDetector()
        self.notifier = TelegramNotifier()
        
        print("✅ Sistema pronto")
        print("=" * 40)
        
    def can_alert(self):
        if self.last_alert is None:
            return True
        return (datetime.now() - self.last_alert) >= self.alert_cooldown
    
    def run(self):
        self.setup()
        print("\n🔴 Monitorando... (q=sair, p=pausa)")
        print("💡 Edite roi.json e reinicie para mudar a área de monitoramento\n")
        
        paused = False
        
        try:
            while True:
                if paused:
                    if cv2.waitKey(100) & 0xFF == ord('p'):
                        paused = False
                        print("▶️ Retomando")
                    continue
                
                ret, frame = self.video_source.read()
                if not ret:
                    if isinstance(self.video_source, FileVideoSource):
                        self.video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    break
                
                self.frame_count += 1
                
                # Processa
                roi_frame = self.roi.apply(frame)
                display = self.roi.draw_on_frame(frame.copy())
                
                # HUD
                h, w = display.shape[:2]
                cv2.putText(display, f"Frames: {self.frame_count}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Detecção
                detected, annotated = self.detector.detect_with_visualization(roi_frame)
                
                if detected:
                    self.detection_count += 1
                    cv2.putText(display, "DOG DETECTED!", (10, 60),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    if self.can_alert():
                        print(f"\n🐶 [{datetime.now().strftime('%H:%M:%S')}] Detecção #{self.detection_count}!")
                        success = self.notifier.send_detection_alert(annotated)
                        if success:
                            self.last_alert = datetime.now()
                            print("📨 Alerta enviado")
                
                cv2.imshow("Smart Yard Dog Monitor", display)
                
                # Controles
                key = cv2.waitKey(30) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('p'):
                    paused = True
                    print("⏸️ Pausado (pressione 'p' para continuar)")
                    
        except KeyboardInterrupt:
            print("\n👋 Encerrado pelo usuário")
        finally:
            self.video_source.release()
            cv2.destroyAllWindows()
            print(f"\n📊 Estatísticas:")
            print(f"   Frames processados: {self.frame_count}")
            print(f"   Detecções: {self.detection_count}")
            print(f"   Alertas enviados: {self.detection_count}")


def main():
    parser = argparse.ArgumentParser(description="Monitor de cães com YOLOv8")
    parser.add_argument("--video", "-v", default="tests/sample.mp4",
                       help="Vídeo, webcam (0,1,2) ou RTSP")
    
    args = parser.parse_args()
    
    monitor = SmartYardMonitor(args.video)
    
    try:
        monitor.run()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()