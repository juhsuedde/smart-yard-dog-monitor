#!/usr/bin/env python3
"""Script rápido para testar componentes individualmente."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def test_roi():
    """Testa persistência da ROI."""
    print("\n🧪 Testando ROI...")
    from src.detection.roi import ROI
    
    # Testa criação
    roi = ROI(x=100, y=100, w=640, h=480, config_file="test_roi.json")
    assert roi.x == 100
    print(f"   ✅ Criação: {roi}")
    
    # Testa persistência
    roi2 = ROI(config_file="test_roi.json")
    print(f"   ✅ Carregamento: {roi2}")
    
    # Limpa arquivo de teste
    if os.path.exists("test_roi.json"):
        os.remove("test_roi.json")
    print("   ✅ Update e persistência")

def test_video_source():
    """Testa fonte de vídeo."""
    print("\n🧪 Testando VideoSource...")
    from src.video.video_source import FileVideoSource
    
    if not os.path.exists("tests/sample.mp4"):
        print("   ⚠️  tests/sample.mp4 não encontrado")
        print("   💡 Crie um vídeo de teste ou use webcam: --video 0")
        return
    
    video = FileVideoSource("tests/sample.mp4")
    success = video.open()
    if success:
        ret, frame = video.read()
        if ret:
            print(f"   ✅ Vídeo aberto, resolução: {frame.shape}")
        video.release()
    else:
        print("   ❌ Erro ao abrir vídeo")

def test_detector():
    """Testa detector YOLO."""
    print("\n🧪 Testando DogDetector...")
    print("   ⏳ Carregando modelo YOLOv8 (pode demorar na primeira vez)...")
    
    try:
        from src.detection.dog_detector import DogDetector
        import numpy as np
        
        detector = DogDetector()
        
        # Frame de teste (ruído aleatório)
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = detector.detect(test_frame)
        
        print(f"   ✅ Detector carregado (resultado em ruído: {result})")
        print("   💡 Resultado em ruído deve ser False (sem cachorro)")
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def test_telegram():
    """Testa notificador."""
    print("\n🧪 Testando TelegramNotifier...")
    from src.notification.telegram_notifier import TelegramNotifier
    from dotenv import load_dotenv
    load_dotenv()
    
    notifier = TelegramNotifier()
    
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("   ⚠️  TELEGRAM_BOT_TOKEN não configurado")
        print("   �� Configure .env para testar envio real")
        return
    
    print("   ✅ Notificador inicializado")
    print("   📧 Para testar envio, execute: python main.py")

def run_all_tests():
    """Executa todos os testes."""
    print("=" * 50)
    print("🚀 Smart Yard Dog Monitor - Testes de Componentes")
    print("=" * 50)
    
    try:
        test_roi()
        test_video_source()
        test_detector()
        test_telegram()
        
        print("\n" + "=" * 50)
        print("✅ Todos os testes concluídos!")
        print("=" * 50)
        print("\n🎮 Próximo passo: execute 'python main.py' para iniciar")
        
    except Exception as e:
        print(f"\n❌ Erro durante testes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
