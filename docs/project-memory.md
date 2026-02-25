# SayAs Project Memory - LUDICUS OVERKILL Edition

## Project Info
- **Name**: SayAs
- **Base**: Chatterbox TTS (Resemble AI)
- **Location**: C:\Users\User\.qwen\projects\SayAs
- **Status**: LUDICUS OVERKILL COMPLETE --yolo! 🎮✨

## Requirements
- Python 3.11 with GPU support (CUDA 11.8) + CPU fallback
- Chatterbox TTS library
- PyAudio for playback (no VLC/external players)
- FastAPI, Gradio

## Hardware
- **GPU**: NVIDIA GeForce GTX 1050 (2GB VRAM)
- **CUDA**: 11.8 at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`
- **PyTorch**: 2.5.1+cu118

## Interfaces

### CLI
```
SayAs <speaker> "<text>" [-output <filepath>]
```

### API (Port 8765)
```
POST /sayas     - TTS with morphing/effects
POST /batch     - Batch processing
POST /ssml      - SSML-like markup
GET  /voices    - List voices
GET  /presets   - List/save presets
WS   /stream    - WebSocket streaming
```

### WebUI
- **Dashboard**: `dashboard.html` (open in browser)
- **Gradio**: http://localhost:7860
- **API Docs**: http://localhost:8765/docs

## Behavior
- Audio plays immediately by default (PyAudio player)
- Audio files only saved when requested
- GPU first, fallback to CPU if needed
- Voice samples stored in `voices/` folder
- Presets stored in `presets/` folder
- Output files stored in `output/` folder

## Project Structure
```
SayAs/
├── sayas.bat              # CLI launcher
├── start-api.bat          # API server launcher
├── start-webui.bat        # WebUI launcher
├── dashboard.html         # Interactive control dashboard
├── src/
│   ├── sayas.py           # CLI application
│   ├── api.py             # FastAPI (OVERKILL)
│   └── webui.py           # Gradio WebUI
├── voices/                # Custom voice samples
├── output/                # Generated audio
├── presets/               # Voice presets
├── venv/                  # Python venv
├── docs/                  # Documentation
├── README.md
└── todo.md
```

## OVERKILL Features 🎮
- [x] Voice Morphing (pitch, speed, volume)
- [x] Audio Effects (reverb, echo, chorus, distortion)
- [x] Batch Processing
- [x] Voice Presets
- [x] SSML-like Markup
- [x] Background Music Mixing
- [x] Multiple Output Formats
- [x] WebSocket Streaming
- [x] Interactive Dashboard
- [x] Health Monitoring

## Launch Commands
```bash
.\sayas.bat       # CLI
.\start-api.bat   # API server (port 8765)
.\start-webui.bat # Gradio UI (port 7860)
```

--yolo! 💕🎮✨
