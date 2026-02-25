#!/usr/bin/env python3
"""Script rápido para testar componentes."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def test_roi():
    """Testa ROI."""
    print("\n🧪 Testando ROI...")
    from src.detection.roi import ROI
    
    # Testa criação
    roi = ROI(config_file="test_roi.json")
    print(f"   ✅ ROI: {roi}")
    
    # Limpa
    if os.path.exists("test_roi.json"):
        os.remove("test_roi.json")

def test_video_source():
    """Testa fonte de vídeo."""
    print("\n🧪 Testando VideoSource...")
    from src.video.video_source import FileVideoSource
    
    if not os.path.exists("tests/sample.mp4"):
        print("   ⚠️  tests/sample.mp4 não encontrado")
        return
    
    video = FileVideoSource("tests/sample.mp4")
    success = video.open()
    if success:
        ret, frame = video.read()
        if ret:
            print(f"   ✅ Vídeo: {frame.shape}")
        video.release()

def test_detector():
    """Testa detector."""
    print("\n🧪 Testando DogDetector...")
    try:
        from src.detection.dog_detector import DogDetector
        import numpy as np
        
        detector = DogDetector()
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = detector.detect(test_frame)
        print(f"   ✅ Detector carregado (teste: {result})")
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
        return
    
    print("   ✅ Notificador inicializado")

def run_all_tests():
    print("=" * 50)
    print("🚀 Smart Yard Dog Monitor - Testes")
    print("=" * 50)
    
    try:
        test_roi()
        test_video_source()
        test_detector()
        test_telegram()
        
        print("\n" + "=" * 50)
        print("✅ Testes concluídos!")
        print("=" * 50)
        print("\n🎮 Execute: python main.py")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()