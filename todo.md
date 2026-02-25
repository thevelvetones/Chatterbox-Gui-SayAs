# SayAs - LUDICUS OVERKILL Edition

## Project Overview
CLI + API + WebUI text-to-speech using Chatterbox with custom voices, voice morphing, audio effects, and more.

**Status**: COMPLETE ✅

---

## Quick Reference

### CLI
```bash
.\listVoices.bat                    # List available voices
SayAs Kate "Hello world"            # Speak with default voice
SayAs Kate "Hello" -output out.wav  # Save to file
```

### API (Port 8765)
```bash
.\start-api.bat   # Start API server
# Docs: http://localhost:8765/docs
```

### WebUI (Port 7860)
```bash
.\start-webui.bat  # Start Gradio UI
# Open: http://localhost:7860
```

### Dashboard
Open `dashboard.html` in browser for full control center.

---

## Features

### Core
- ✅ Default Chatterbox TTS voice
- ✅ Custom voice cloning (.wav/.mp3 samples)
- ✅ GPU accelerated (GTX 1050) + CPU fallback
- ✅ PyAudio playback (no external players)

### OVERKILL (API)
- ✅ Voice Morphing (pitch, speed, volume)
- ✅ Audio Effects (reverb, echo, chorus, distortion)
- ✅ Batch Processing
- ✅ Voice Presets
- ✅ SSML-like Markup
- ✅ Background Music Mixing
- ✅ Multiple Formats (wav, mp3, flac, ogg)
- ✅ WebSocket Streaming

### UI
- ✅ CLI with simple syntax
- ✅ Gradio WebUI (pink notebook theme)
- ✅ Interactive HTML Dashboard
- ✅ API with Swagger docs

---

## Project Structure

```
SayAs/
├── sayas.bat           # CLI launcher
├── listVoices.bat      # List voices
├── start-api.bat       # API server
├── start-webui.bat     # Gradio UI
├── dashboard.html      # Control dashboard
├── src/
│   ├── sayas.py        # CLI app
│   ├── api.py          # FastAPI server
│   └── webui.py        # Gradio UI
├── voices/             # Custom voice samples
├── output/             # Generated audio
├── presets/            # Voice presets
├── venv/               # Python virtual environment
├── docs/               # Documentation
├── README.md
└── todo.md
```

---

## Hardware

- **GPU**: NVIDIA GTX 1050 (2GB VRAM)
- **CUDA**: 11.8
- **PyTorch**: 2.5.1+cu118
- **Python**: 3.11

---

## Git History

```
c7cbf8a Fix WebUI dropdown voice handling
9faec13 Add listVoices.bat
385f6b0 Final polish: README + project memory
7bf3049 LUDICUS OVERKILL update
c7f99f9 Initial commit: SayAs CLI v1.0
```

---

## Notes

- Audio plays immediately by default (CLI/WebUI)
- API has multiple output modes (play, return, both, save)
- Voice samples go in `voices/` folder
- Presets saved to `presets/` folder
- All docs in `/docs` as .md files

---

**--yolo! 💕🎮✨**

*Made with love and way too many features*
