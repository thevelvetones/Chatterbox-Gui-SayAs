# SayAs Project Memory

## Project Info

- **Name**: SayAs - LUDICUS OVERKILL Edition 💕🎮
- **Base**: Chatterbox TTS (Resemble AI)
- **Location**: `C:\Users\User\.qwen\projects\SayAs`
- **Status**: COMPLETE ✅
- **Version**: 3.0.0-OVERKILL

---

## Hardware Configuration

| Component | Specification |
|-----------|---------------|
| **GPU** | NVIDIA GeForce GTX 1050 (2GB VRAM) |
| **CUDA** | 11.8 at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8` |
| **PyTorch** | 2.5.1+cu118 |
| **Python** | 3.11 |
| **OS** | Windows 10/11 |

---

## Interfaces

### CLI (Command Line)

```bash
.\listVoices.bat                        # List available voices
SayAs <speaker> "<text>"                # Speak with default output
SayAs <speaker> "<text>" -output <file> # Save to file
```

### API Server (Port 8765)

```bash
.\start-api.bat
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /` | GET | API info and features |
| `GET /voices` | GET | List available voices |
| `POST /sayas` | POST | Generate speech with all options |
| `POST /batch` | POST | Batch processing |
| `POST /ssml` | POST | SSML-like advanced control |
| `GET /presets` | GET | List presets |
| `POST /presets` | POST | Save preset |
| `GET /presets/{name}` | GET | Load specific preset |
| `GET /health` | GET | Health check |
| `WS /stream` | WS | WebSocket streaming |
| `GET /docs` | - | Swagger UI |

### WebUI (Port 7860)

```bash
.\start-webui.bat
# Open: http://localhost:7860
```

Features:
- Pink notebook-themed Gradio interface
- Voice selection dropdown
- Text input with server playback option
- Audio download capability

### Dashboard

Open `dashboard.html` in browser for full control center with:
- Real-time API status monitoring
- Voice morphing controls
- Audio effects toggles
- Background music mixing
- Preset management
- Batch processing
- Activity logging

---

## Project Structure

```
SayAs/
├── sayas.bat              # CLI launcher
├── listVoices.bat         # List voices utility
├── start-api.bat          # API server launcher
├── start-webui.bat        # Gradio WebUI launcher
├── dashboard.html         # Control dashboard (pink theme)
├── README.md              # Project readme
├── src/
│   ├── sayas.py           # CLI application
│   ├── api.py             # FastAPI server (OVERKILL features)
│   └── webui.py           # Gradio WebUI (pink notebook theme)
├── voices/                # Custom voice samples (.wav, .mp3)
├── output/                # Generated audio files
├── presets/               # Voice preset JSON files
├── venv/                  # Python virtual environment
└── docs/                  # Documentation
    ├── usage.md           # Complete usage guide
    ├── api-reference.md   # API endpoint documentation
    ├── webui-guide.md     # WebUI user guide
    └── project-memory.md  # This file
```

---

## Features

### Core TTS
- ✅ Default Chatterbox voice
- ✅ Custom voice cloning from .wav/.mp3 samples
- ✅ GPU acceleration (GTX 1050) with CPU fallback
- ✅ Multiple output formats (WAV, MP3, FLAC, OGG)

### OVERKILL Features 🎮

| Feature | Description |
|---------|-------------|
| **Voice Morphing** | Pitch (0.5-2.0), Speed (0.5-2.0), Volume (0.1-2.0) |
| **Audio Effects** | Reverb, Echo, Chorus, Distortion, Normalize |
| **Batch Processing** | Process multiple texts in single API call |
| **Voice Presets** | Save/load complete voice configurations |
| **SSML-like Control** | Segment-by-segment advanced control |
| **Background Music** | Mix music with speech (adjustable volume) |
| **WebSocket Streaming** | Real-time TTS streaming |
| **Interactive Dashboard** | Beautiful pink control center |
| **Swagger UI** | Interactive API documentation |

---

## Pydantic Models

### VoiceMorphing
```python
class VoiceMorphing(BaseModel):
    pitch: float = 1.0      # 0.5 to 2.0
    speed: float = 1.0      # 0.5 to 2.0
    volume: float = 1.0     # 0.0 to 2.0
```

### AudioEffects
```python
class AudioEffects(BaseModel):
    reverb: bool = False
    reverb_amount: float = 0.3
    echo: bool = False
    echo_delay: float = 0.3
    chorus: bool = False
    chorus_amount: float = 0.3
    distortion: bool = False
    distortion_amount: float = 0.1
    normalize: bool = True
```

### SayAsRequest
```python
class SayAsRequest(BaseModel):
    voice: str
    text: str
    output_mode: Literal["play", "return", "both", "save"]
    use_custom_voice: bool = True
    morphing: Optional[VoiceMorphing] = None
    effects: Optional[AudioEffects] = None
    output_format: Literal["wav", "mp3", "flac", "ogg"] = "wav"
    save_path: Optional[str] = None
    background_music: Optional[str] = None
    background_volume: float = 0.3
```

---

## User Preferences (Lief)

- **Name**: Lief
- **Default projects folder**: `C:\Users\User\.qwen\projects`
- **No background jobs** without prior notification
- **Project structure**: Each project should have `todo.md` and `/docs` folder
- **Documentation**: All docs in .md format stored in `/docs`
- **Output language**: English

---

## Quick Reference

### Start Commands
```bash
.\start-api.bat      # Start API server (port 8765)
.\start-webui.bat    # Start WebUI (port 7860)
.\listVoices.bat     # List available voices
SayAs Kate "Hello"   # CLI usage
```

### URLs
- API: http://localhost:8765
- Swagger Docs: http://localhost:8765/docs
- WebUI: http://localhost:7860
- Dashboard: Open `dashboard.html` in browser

### Voice Sample Location
```
C:\Users\User\.qwen\projects\SayAs\voices\
```

### Preset Location
```
C:\Users\User\.qwen\projects\SayAs\presets\
```

### Output Location
```
C:\Users\User\.qwen\projects\SayAs\output\
```

---

## Performance

| Hardware | Time per Short Sentence |
|----------|------------------------|
| GTX 1050 (GPU) | ~3-5 seconds |
| CPU (fallback) | ~10-15 seconds |

---

## Dependencies

```
chatterbox-tts
pyaudio
fastapi
uvicorn
gradio
torch
torchaudio
numpy
pydantic
```

---

## Version History

| Version | Codename | Features |
|---------|----------|----------|
| 1.0 | Base | CLI TTS with custom voice support |
| 2.0 | WebUI | Added Gradio interface |
| 3.0 | OVERKILL | Voice morphing, effects, batch, presets, SSML, streaming |

---

**--yolo! 💕🎮✨**

*Made with excessive love and too many features*
