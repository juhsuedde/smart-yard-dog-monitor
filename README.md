# smart-yard-dog-monitor

Esse projeto usa visão computacional para detectar cães em uma área definida de vídeo e disparar alertas de forma controlada.

## Por que fiz esse projeto?

Queria explorar visão computacional em um caso prático: monitorar uma área usando câmera e detectar especificamente quando um cachorro entra nessa zona.  
Foi uma forma de aprender como integrar modelos de detecção de objetos (YOLOv8) com lógica de alerta e evitar notificações repetidas.

## O que ele faz hoje

- Captura frames de uma fonte de vídeo (como webcam ou stream)
- Usa um modelo YOLOv8 para detectar apenas a classe **“dog”**
- Monitora uma região de interesse (ROI) definida no vídeo
- Dispara um alerta sempre que um cachorro entra na ROI
- Evita alertas repetidos com um sistema de cooldown

## Como funciona

O código está organizado com base nas principais responsabilidades:

1. **Captura de vídeo:** o loop principal lê os frames continuamente.
2. **Detecção de objeto:** o modelo YOLOv8 analisa cada frame e identifica cães.
3. **Região de interesse (ROI):** você pode delimitar no código a área que importa monitorar.
4. **Alertas com cooldown:** quando o cachorro entra na ROI, um alerta é enviado; se ele permanecer lá, o cooldown impede notificações constantes.

## Estrutura do projeto

- `src/detector.py`: lógica que usa o modelo de detecção
- `src/main.py`: loop principal que captura o vídeo e aplica a detecção
- `src/test_video_source.py`: utilitário para testar a fonte de vídeo
- `tests/`: testes automatizados (se houver)
- `.env.example`: exemplo de variáveis de ambiente para configuração

## O que ainda quero melhorar

- Tornar mais configurável (ROI via interface ou arquivo de configuração)
- Adicionar notificações mais visuais ou via serviço externo
- Estruturar testes automáticos mais abrangentes

## Tecnologias usadas

- Python
- YOLOv8 (detecção de objetos)
- OpenCV (captura e processamento de vídeo)

## Como testar

1. Configure a fonte de vídeo (webcam ou stream)
2. Ajuste a ROI se necessário
3. Execute o projeto com Python

```bash
python src/main.py
```
