import cv2
import os
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.video.video_source import FileVideoSource, WebcamVideoSource, RTSPVideoSource
from src.detection.dog_detector import DogDetector
from src.detection.roi import ROI
from src.detection.roi_selector import ROISelector
from src.notification.telegram_notifier import TelegramNotifier

# Carrega variáveis de ambiente
load_dotenv()

class SmartYardMonitor:
    """Sistema principal de monitoramento."""
    
    def __init__(self, video_path: str = "tests/sample.mp4", use_interactive_roi: bool = False):
        self.video_path = video_path
        self.use_interactive_roi = use_interactive_roi
        
        # Componentes
        self.video_source = None
        self.roi = None
        self.detector = None
        self.notifier = None
        
        # Controle de alertas (cooldown)
        self.last_alert_time = None
        self.alert_cooldown = timedelta(minutes=5)  # 5 minutos entre alertas
        self.alert_count = 0
        
        # Estatísticas
        self.frames_processed = 0
        self.detections_count = 0
        self.start_time = None
        
    def setup(self):
        """Configura todos os componentes."""
        print("\n🚀 Iniciando Smart Yard Dog Monitor v2.0")
        print("=" * 50)
        
        # 1. Fonte de vídeo
        if self.video_path.startswith("rtsp://"):
            self.video_source = RTSPVideoSource(self.video_path)
        elif self.video_path.isdigit() or self.video_path in ["0", "1", "2"]:
            self.video_source = WebcamVideoSource(int(self.video_path))
        else:
            self.video_source = FileVideoSource(self.video_path)
        
        if not self.video_source.open():
            raise RuntimeError("Não foi possível abrir fonte de vídeo")
        
        # 2. ROI - Interativa ou arquivo
        if self.use_interactive_roi:
            print("\n🖱️  Modo de seleção interativa de ROI")
            selector = ROISelector()
            roi = selector.select_from_video(self.video_source)
            if roi:
                self.roi = roi
            else:
                print("⚠️  Nenhuma ROI selecionada, usando padrão")
                self.roi = ROI()
        else:
            self.roi = ROI()  # Carrega de roi.json ou cria padrão
        
        print(f"📐 ROI configurada: {self.roi}")
        
        # 3. Detector
        self.detector = DogDetector()
        
        # 4. Notificador
        self.notifier = TelegramNotifier()
        
        print("=" * 50)
        print("✅ Sistema pronto para monitoramento\n")
        
    def should_send_alert(self) -> bool:
        """Verifica se pode enviar alerta respeitando cooldown."""
        if self.last_alert_time is None:
            return True
        
        elapsed = datetime.now() - self.last_alert_time
        return elapsed >= self.alert_cooldown
    
    def process_frame(self, frame):
        """Processa um frame: aplica ROI, detecta e alerta."""
        self.frames_processed += 1
        
        # Aplica ROI
        roi_frame = self.roi.apply(frame)
        
        # Desenha ROI no frame original para visualização
        display_frame = self.roi.draw_on_frame(frame.copy())
        
        # Adiciona informações na tela (HUD)
        self._draw_hud(display_frame)
        
        # Detecção
        detected, annotated_roi = self.detector.detect_with_visualization(roi_frame)
        
        if detected:
            self.detections_count += 1
            
            # Indica detecção no display
            cv2.putText(display_frame, "🐶 CACHORRO DETECTADO!", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Envia alerta se respeitar cooldown
            if self.should_send_alert():
                print(f"\n🐶 [{datetime.now().strftime('%H:%M:%S')}] Cachorro detectado!")
                
                # Envia foto do flagrante
                success = self.notifier.send_detection_alert(
                    annotated_roi, 
                    roi_name=f"ROI ({self.roi.x},{self.roi.y})"
                )
                
                if success:
                    self.last_alert_time = datetime.now()
                    self.alert_count += 1
                    print(f"📨 Alerta #{self.alert_count} enviado")
                    
                    # Também envia mensagem de texto como backup
                    self.notifier.send(
                        f"🚨 <b>Alerta de Intruso!</b>\n"
                        f"🐶 Cachorro detectado no quintal\n"
                        f"📍 ROI: {self.roi}\n"
                        f"🕐 {datetime.now().strftime('%H:%M:%S')}"
                    )
                else:
                    print("⚠️  Falha ao enviar alerta")
        
        return display_frame, detected
    
    def _draw_hud(self, frame):
        """Desenha interface de informações no frame."""
        h, w = frame.shape[:2]
        
        # Painel superior
        cv2.rectangle(frame, (0, 0), (w, 30), (0, 0, 0), -1)
        
        # FPS e contadores
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        fps = self.frames_processed / max(elapsed, 1)
        
        status_text = f"FPS:{fps:.1f} | Frames:{self.frames_processed} | Detecções:{self.detections_count}"
        cv2.putText(frame, status_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Status do último alerta
        if self.last_alert_time:
            time_since = (datetime.now() - self.last_alert_time).total_seconds()
            mins, secs = divmod(int(time_since), 60)
            alert_text = f"Último alerta: {mins}m {secs}s atrás"
            color = (0, 255, 0) if time_since > 300 else (0, 165, 255)
        else:
            alert_text = "Sem alertas ainda"
            color = (128, 128, 128)
        
        cv2.putText(frame, alert_text, (w - 250, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Instruções
        cv2.putText(frame, "'q'=sair | 'r'=redefinir ROI | 'p'=pausa", 
                   (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Loop principal de execução."""
        self.start_time = datetime.now()
        paused = False
        
        print("🔴 Monitoramento iniciado")
        print("   Pressione 'q' para sair, 'r' para redefinir ROI, 'p' para pausar\n")
        
        try:
            while True:
                if not paused:
                    ret, frame = self.video_source.read()
                    
                    if not ret or frame is None:
                        # Se for vídeo de arquivo, reinicia
                        if isinstance(self.video_source, FileVideoSource):
                            print("🔄 Vídeo terminou, reiniciando...")
                            self.video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
                            continue
                        else:
                            print("⚠️  Frame inválido, tentando novamente...")
                            time.sleep(0.1)
                            continue
                    
                    # Processa frame
                    display_frame, detected = self.process_frame(frame)
                    
                    # Mostra resultado
                    cv2.imshow("Smart Yard Dog Monitor", display_frame)
                
                # Controles
                key = cv2.waitKey(30) & 0xFF
                
                if key == ord('q'):
                    print("\n👋 Encerrando monitoramento...")
                    break
                    
                elif key == ord('p'):
                    paused = not paused
                    print(f"{'⏸️' if paused else '▶️'} {'Pausado' if paused else 'Retomando'}")
                    
                elif key == ord('r'):
                    print("\n🖱️  Redefinindo ROI...")
                    cv2.destroyWindow("Smart Yard Dog Monitor")
                    selector = ROISelector()
                    new_roi = selector.select_from_video(self.video_source)
                    if new_roi:
                        self.roi = new_roi
                        print(f"✅ Nova ROI: {self.roi}")
                    else:
                        print("⚠️  ROI não alterada")
                    
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido pelo usuário")
            
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Libera recursos e mostra estatísticas."""
        print("\n📊 Estatísticas Finais:")
        print(f"   Frames processados: {self.frames_processed}")
        print(f"   Detecções: {self.detections_count}")
        print(f"   Alertas enviados: {self.alert_count}")
        
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            print(f"   Duração: {duration:.1f}s")
            print(f"   Média FPS: {self.frames_processed/max(duration, 1):.1f}")
        
        if self.video_source:
            self.video_source.release()
        cv2.destroyAllWindows()
        print("\n✅ Sistema encerrado")

def main():
    """Entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Smart Yard Dog Monitor")
    parser.add_argument("--video", "-v", default="tests/sample.mp4", 
                       help="Caminho do vídeo ou ID da webcam (0, 1, 2) ou URL RTSP")
    parser.add_argument("--interactive-roi", "-i", action="store_true",
                       help="Permite selecionar ROI interativamente no início")
    parser.add_argument("--reset-roi", "-r", action="store_true",
                       help="Reseta ROI para padrão antes de iniciar")
    
    args = parser.parse_args()
    
    # Reseta ROI se solicitado
    if args.reset_roi and os.path.exists("roi.json"):
        os.remove("roi.json")
        print("🗑️  ROI resetada")
    
    # Cria e executa monitor
    monitor = SmartYardMonitor(
        video_path=args.video,
        use_interactive_roi=args.interactive_roi
    )
    
    try:
        monitor.setup()
        monitor.run()
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()