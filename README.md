# Smart Yard Dog Monitor 🐶

Projeto de visão computacional desenvolvido em Python para **monitorar uma área específica de um ambiente** e **alertar quando um cachorro entra nessa área**, utilizando detecção por IA em tempo real.

A ideia surgiu a partir de uma necessidade real de **segurança**, mas o sistema foi pensado de forma **genérica**, podendo ser adaptado para qualquer área monitorada.

---

## 🎯 Objetivo do projeto

Detectar a presença de um cachorro em uma região delimitada do vídeo e gerar um alerta **sem spam**, mesmo que o animal permaneça no local por um período prolongado.

O foco do projeto é:

- Arquitetura clara
- Código legível
- Boas práticas
- Aplicação prática de Inteligência Artificial

---

## 🧠 Como funciona

1. O sistema captura frames de uma fonte de vídeo (webcam ou stream).
2. Um modelo **YOLOv8** é usado para detectar apenas a classe **dog**.
3. Uma **região de interesse (ROI)** é definida no frame.
4. Caso o cachorro entre nessa área:
   - Um alerta é disparado
   - Um **cooldown** evita notificações repetidas
5. O sistema continua monitorando em tempo real.

---

## 🧱 Estrutura do projeto

```text
src/
 ├── detector.py          Lógica de detecção com YOLO
 ├── main.py              Loop principal + ROI + cooldown
 ├── test_video_source.py Teste isolado da fonte de vídeo
tests/
architecture.md           Documentação da arquitetura
.env.example              Exemplo de variáveis de ambiente
```
