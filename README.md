# SayAs - LUDICUS OVERKILL Edition 💕🎮

**The most extra text-to-speech system you never knew you needed!**

## Quick Start

### List Voices
```bash
.\listVoices.bat
```

### CLI
```bash
SayAs Kate "This is what I want Kate to say in Kate Voice"
SayAs Kate "Hello" -output greeting.wav
```

### API Server
```bash
.\start-api.bat
# API: http://localhost:8765
# Docs: http://localhost:8765/docs
```

### WebUI
```bash
.\start-webui.bat
# Open: http://localhost:7860
```

### Dashboard
Open `dashboard.html` in your browser for the full control center!

## Features 🎮

### Core TTS
- ✅ Default Chatterbox voice
- ✅ Custom voice cloning from .wav/.mp3 samples
- ✅ GPU accelerated (GTX 1050) with CPU fallback

### OVERKILL Features
- 🎛️ **Voice Morphing**: Pitch, speed, volume control
- 🎨 **Audio Effects**: Reverb, echo, chorus, distortion
- 📦 **Batch Processing**: Process multiple texts at once
- 💾 **Voice Presets**: Save and load configurations
- 📝 **SSML Support**: Advanced segment-by-segment control
- 🎵 **Background Music**: Mix music with speech
- 📀 **Multiple Formats**: WAV, MP3, FLAC, OGG
- 🔌 **WebSocket**: Real-time streaming
- 🎯 **Interactive Dashboard**: Beautiful control center

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sayas` | POST | Generate speech with all options |
| `/batch` | POST | Batch process multiple texts |
| `/ssml` | POST | SSML-like advanced control |
| `/voices` | GET | List available voices |
| `/presets` | GET/POST | List or save presets |
| `/stream` | WS | WebSocket streaming |
| `/health` | GET | Health check |

## Example API Request

```json
POST http://localhost:8765/sayas
{
  "voice": "Kate",
  "text": "Hello world!",
  "output_mode": "both",
  "morphing": {
    "pitch": 1.2,
    "speed": 1.0,
    "volume": 1.0
  },
  "effects": {
    "reverb": true,
    "echo": false,
    "chorus": false,
    "distortion": false,
    "normalize": true
  }
}
```

## Project Structure

```
SayAs/
├── sayas.bat           # CLI launcher
├── start-api.bat       # API server
├── start-webui.bat     # Gradio UI
├── dashboard.html      # Control dashboard
├── src/
│   ├── sayas.py        # CLI app
│   ├── api.py          # FastAPI server
│   └── webui.py        # Gradio UI
├── voices/             # Voice samples
├── output/             # Generated audio
├── presets/            # Voice presets
└── docs/               # Documentation
```

## Hardware Requirements

- **GPU**: NVIDIA GTX 1050 or better (CUDA 11.8)
- **CPU**: Fallback mode available (slower)
- **RAM**: 8GB+ recommended

## Installation

The project comes with a pre-configured virtual environment. If you need to reinstall:

```bash
cd C:\Users\User\.qwen\projects\SayAs
.\venv\Scripts\activate
pip install chatterbox-tts pyaudio fastapi uvicorn gradio
```

## Full Documentation

See [docs/usage.md](docs/usage.md) for complete usage guide.

---

**--yolo! 💕🎮✨**

*Made with excessive love and too many features*
