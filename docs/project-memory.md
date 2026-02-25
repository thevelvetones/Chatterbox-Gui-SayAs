# SayAs Project Memory

## Project Info
- **Name**: SayAs
- **Base**: Chatterbox TTS (Resemble AI)
- **Location**: `C:\Users\User\.qwen\projects\SayAs`
- **Status**: COMPLETE ✅

## Hardware
- **GPU**: NVIDIA GeForce GTX 1050 (2GB VRAM)
- **CUDA**: 11.8 at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`
- **PyTorch**: 2.5.1+cu118
- **Python**: 3.11

## Interfaces

### CLI
```bash
.\listVoices.bat                        # List voices
SayAs <speaker> "<text>"                # Speak
SayAs <speaker> "<text>" -output <file> # Save to file
```

### API (Port 8765)
```bash
.\start-api.bat
# POST /sayas   - Generate speech
# POST /batch   - Batch processing
# GET  /voices  - List voices
# GET  /presets - List/save presets
# WS   /stream  - WebSocket streaming
# GET  /docs    - Swagger UI
```

### WebUI (Port 7860)
```bash
.\start-webui.bat
# Open: http://localhost:7860
```

### Dashboard
Open `dashboard.html` in browser.

## Project Structure
```
SayAs/
├── sayas.bat           # CLI
├── listVoices.bat      # List voices
├── start-api.bat       # API
├── start-webui.bat     # WebUI
├── dashboard.html      # Dashboard
├── src/
│   ├── sayas.py        # CLI app
│   ├── api.py          # FastAPI
│   └── webui.py        # Gradio
├── voices/             # Voice samples
├── output/             # Generated audio
├── presets/            # Presets
├── venv/               # Virtual environment
└── docs/               # Documentation
```

## Features
- Default + custom voice TTS
- GPU acceleration with CPU fallback
- Voice morphing (pitch, speed, volume)
- Audio effects (reverb, echo, chorus, distortion)
- Batch processing
- Voice presets
- Multiple output formats
- WebSocket streaming
- Interactive dashboard

## User Preferences
- Name: Lief
- Default projects: `C:\Users\User\.qwen\projects`
- No background jobs without notification
- Projects should have `todo.md` and `/docs` folder
- All docs in .md format

---

**--yolo! 💕🎮✨**
