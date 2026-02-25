# SayAs - LUDICUS OVERKILL Edition 💕🎮

## Project Overview
CLI + API + WebUI + **Desktop App** text-to-speech using Chatterbox with custom voices, voice morphing, audio effects, and more.

**Current Status**: Electron Desktop App Working! 🚀

---

## Completed ✅

### Long Text Support
- ✅ Text splitter utility with sentence-aware chunking
- ✅ Audio stitching with configurable silence gaps
- ✅ CLI auto-split for 900+ char texts
- ✅ API auto-split with response flag
- ✅ Abbreviation handling (Mr., Dr., St., etc.)

### WebUI Voice Upload
- ✅ Name input field for new voices
- ✅ File upload for .wav/.mp3 audio files
- ✅ Save button to store voices
- ✅ Voice list display
- ✅ Delete functionality

### Electron Desktop App
- ✅ Main process (window + Python backend management)
- ✅ Preload script (secure IPC)
- ✅ Renderer (loading screen with pink theme)
- ✅ electron-builder configuration
- ✅ Build scripts for Windows
- ✅ App icon (SVG)
- ✅ **WORKING**: Tested and generates speech!

---

## In Progress 🚧

### UI Improvements
- [ ] Tab-based layout (Generator | Create Voice | API/Connect)
- [ ] Keep model in RAM (don't exit after generation)
- [ ] Start API server on app launch
- [ ] Add API connection details in 3rd tab

### Final Steps
- [ ] Build Windows installer
- [ ] Test standalone .exe
- [ ] Update all documentation

---

## Quick Reference

### CLI
```bash
.\listVoices.bat                    # List available voices
SayAs Kate "Hello world"            # Speak with default voice
SayAs Kate "Hello" -output out.wav  # Save to file
SayAs Kate "Long text..."           # Auto-splits if 900+ chars!
```

### API (Port 8765)
```bash
.\start-api.bat
# Docs: http://localhost:8765/docs
```

### WebUI (Port 7860)
```bash
.\start-webui.bat
# Open: http://localhost:7860
```

### Electron App (NEW!)
```bash
cd electron-app
.\start.bat          # Development
.\build.bat          # Build installer
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
- ✅ **Long text auto-splitting** (900+ chars)

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
- ✅ **Electron Desktop App** (Windows .exe)

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
│   ├── webui.py        # Gradio UI (with voice upload!)
│   └── text_splitter.py # Long text handling
├── voices/             # Custom voice samples
├── output/             # Generated audio
├── presets/            # Voice presets
├── venv/               # Python virtual environment
├── docs/               # Documentation
│   ├── usage.md
│   ├── api-reference.md
│   ├── webui-guide.md
│   ├── project-memory.md
│   └── index.html      # Pink notebook docs site
├── electron-app/       # NEW! Desktop app
│   ├── src/
│   │   ├── main/
│   │   ├── preload/
│   │   └── renderer/
│   ├── assets/
│   ├── package.json
│   ├── build.bat
│   └── start.bat
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
50dfb6d Electron app working! 💕🎮
809c7a1 Add Electron app build config and gitignore 💕
6ceb3a5 Added WebUI voice upload feature 💕
66cd2f4 Electron Desktop App structure 💕🎮
849d03e Add long text support with auto-splitting 💕
```

---

## Notes

- Audio plays immediately by default (CLI/WebUI)
- API has multiple output modes (play, return, both, save)
- Voice samples go in `voices/` folder
- Presets saved to `presets/` folder
- All docs in `/docs` as .md files
- Long text (900+ chars) auto-splits with custom voices
- 0.5s silence between chunks by default
- **NEW**: WebUI has voice upload feature!
- **NEW**: Electron desktop app - WORKING!

---

## Building the Electron App

### 1. Install Dependencies
```bash
cd electron-app
npm install
```

### 2. Run in Development
```bash
.\start.bat
```

### 3. Build Windows Installer
```bash
.\build.bat
```

Installer will be in `electron-app/dist/`

---

**--yolo! 💕🎮✨**

*Made with excessive love and way too many features*
