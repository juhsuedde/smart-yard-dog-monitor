# smart-yard-dog-monitor

Sistema de monitoramento inteligente para detectar cães em áreas específicas usando visão computacional (YOLOv8) e enviar alertas via Telegram.

## Por que fiz esse projeto?

Queria explorar visão computacional em um caso prático: monitorar uma área usando câmera e detectar especificamente quando um cachorro entra nessa zona.  
Foi uma forma de aprender como integrar modelos de detecção de objetos (YOLOv8) com lógica de alerta e evitar notificações repetidas.

## O que ele faz hoje

- Captura frames de uma fonte de vídeo (como webcam ou stream)
- Usa um modelo YOLOv8 para detectar apenas a classe **“dog”**
- Monitora uma região de interesse (ROI) definida via arquivo JSON
- Dispara um alerta sempre que um cachorro entra na ROI
- Evita alertas repetidos com um sistema de cooldown

## Como funciona

O código está organizado com base nas principais responsabilidades:

1. **Captura de vídeo:** o loop principal lê os frames continuamente.
2. **Detecção de objeto:** o modelo YOLOv8 analisa cada frame e identifica cães.
3. **Região de interesse (ROI):** você pode delimitar no código a área que importa monitorar.
4. **Alertas com cooldown:** quando o cachorro entra na ROI, um alerta é enviado; se ele permanecer lá, o cooldown impede notificações constantes.

## Estrutura do projeto

- `main.py`: entry point com CLI e loop principal
- `headless_mode.py`: versão sem interface para rodar em servidor
- `roi.json`: configuração da região de interesse (x, y, w, h)
- `src/video/video_source.py`: FileVideoSource, WebcamVideoSource, RTSPVideoSource
- `src/detection/roi.py`: carrega e aplica ROI do JSON
- `src/detection/dog_detector.py`: detecção com YOLOv8
- `src/notification/telegram_notifier.py`: envio de alertas
- `tests/`: vídeos de teste
- `.env`: variáveis do Telegram (token e chat_id)

## O que ainda quero melhorar

- Tornar a configuração da ROI mais prática (atualmente edito o JSON manualmente)
- Adicionar testes automatizados mais abrangentes

## Tecnologias usadas

- Python
- YOLOv8 (detecção de objetos)
- OpenCV (captura e processamento de vídeo)

## Como testar

1. Configure a ROI editando roi.json
2. Execute o projeto com Python

```bash
python main.py
```
