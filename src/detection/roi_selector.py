import cv2
import numpy as np
from typing import Optional, Callable
from src.detection.roi import ROI

class ROISelector:
    """Interface interativa para seleção de ROI usando mouse."""
    
    def __init__(self, window_name: str = "Selecione a ROI"):
        self.window_name = window_name
        self.drawing = False
        self.start_x, self.start_y = -1, -1
        self.end_x, self.end_y = -1, -1
        self.current_frame = None
        self.original_frame = None
        self.roi_callback: Optional[Callable] = None
        
    def mouse_callback(self, event, x, y, flags, param):
        """Callback do mouse para desenhar retângulo."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_x, self.start_y = x, y
            self.end_x, self.end_y = x, y
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.end_x, self.end_y = x, y
                # Redesenha frame original com retângulo temporário
                temp_frame = self.original_frame.copy()
                cv2.rectangle(temp_frame, 
                            (self.start_x, self.start_y), 
                            (self.end_x, self.end_y), 
                            (0, 255, 255), 2)
                # Mostra dimensões
                w = abs(self.end_x - self.start_x)
                h = abs(self.end_y - self.start_y)
                cv2.putText(temp_frame, f"{w}x{h}", 
                          (min(self.start_x, self.end_x), min(self.start_y, self.end_y) - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.imshow(self.window_name, temp_frame)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_x, self.end_y = x, y
            
            # Garante coordenadas corretas (start < end)
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)
            
            w = x2 - x1
            h = y2 - y1
            
            if w > 50 and h > 50:  # ROI mínima de 50x50
                roi = ROI(x1, y1, w, h)
                if self.roi_callback:
                    self.roi_callback(roi)
                print(f"✅ ROI definida: ({x1}, {y1}, {w}, {h})")
            else:
                print("⚠️ ROI muito pequena. Selecione uma área maior.")
    
    def select_from_video(self, video_source, max_frames: int = 30) -> Optional[ROI]:
        """
        Abre o vídeo e permite selecionar ROI interativamente.
        Retorna a ROI selecionada ou None se cancelado.
        """
        print("🖱️  Modo de seleção de ROI")
        print("   Clique e arraste para definir a área de monitoramento")
        print("   Pressione 'q' para cancelar, 's' para usar ROI atual")
        
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
        selected_roi = None
        frame_count = 0
        
        try:
            while True:
                ret, frame = video_source.read()
                if not ret or frame is None:
                    break
                
                self.original_frame = frame.copy()
                
                # Instruções na tela
                display_frame = frame.copy()
                cv2.putText(display_frame, "Clique e arraste para definir ROI", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(display_frame, "'q' = cancelar | 's' = salvar", 
                          (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.imshow(self.window_name, display_frame)
                
                key = cv2.waitKey(30) & 0xFF
                if key == ord('q'):
                    print("❌ Seleção cancelada")
                    break
                elif key == ord('s'):
                    if selected_roi:
                        print("✅ ROI salva")
                        break
                    else:
                        print("⚠️ Nenhuma ROI selecionada ainda")
                
                frame_count += 1
                if frame_count >= max_frames:
                    frame_count = 0
                    video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    
        finally:
            cv2.destroyWindow(self.window_name)
        
        return selected_roi
    
    def select_from_image(self, image_path: str) -> Optional[ROI]:
        """Seleciona ROI a partir de uma imagem estática."""
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"❌ Erro ao carregar imagem: {image_path}")
            return None
        
        self.original_frame = frame.copy()
        
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
        print("🖼️  Selecione a ROI na imagem")
        print("   Clique e arraste para definir")
        print("   Pressione 'q' para sair")
        
        selected_roi = None
        
        def save_roi(roi):
            nonlocal selected_roi
            selected_roi = roi
        
        self.roi_callback = save_roi
        
        while True:
            display_frame = self.original_frame.copy()
            cv2.putText(display_frame, "Defina a ROI e pressione 'q'", 
                      (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow(self.window_name, display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyWindow(self.window_name)
        return selected_roi
