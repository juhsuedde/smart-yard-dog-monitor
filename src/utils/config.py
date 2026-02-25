"""Configurações e utilitários do sistema."""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"
TESTS_DIR = BASE_DIR / "tests"

# ROI
ROI_CONFIG_FILE = BASE_DIR / "roi.json"
DEFAULT_ROI = {"x": 200, "y": 150, "w": 800, "h": 400}

# Detecção
CONFIDENCE_THRESHOLD = 0.5
DOG_CLASS_ID = 16  # COCO dataset

# Alertas
ALERT_COOLDOWN_MINUTES = 5
MAX_ALERTS_PER_HOUR = 12

# Telegram (carregado de .env)
def get_telegram_config():
    """Retorna configurações do Telegram do ambiente."""
    return {
        "bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
        "chat_id": os.getenv("TELEGRAM_CHAT_ID")
    }

# Vídeo
DEFAULT_VIDEO_PATH = TESTS_DIR / "sample.mp4"
FRAME_SKIP = 1  # Processar todos os frames (1 = sem skip)
