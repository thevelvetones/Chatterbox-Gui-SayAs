# SayAs - LUDICUS OVERKILL Edition 💕🎮

## Project Overview
CLI + API + WebUI + **Desktop App** text-to-speech using Chatterbox with custom voices, voice morphing, audio effects, and more.

**Current Status**: BUILT AND WORKING! 🚀✅

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
- ✅ **BUILT**: Windows executable created!

### UI Improvements
- ✅ Tab-based layout (4 tabs!)
  - 🎤 Voice Generator
  - 🎙️ Create New Voice
  - 🔌 API & Connect
  - 📖 Documentation (embedded docs/index.html)
- ✅ Input clears after generation (model stays in RAM)
- ✅ API server starts automatically with app
- ✅ App only exits when user clicks X

---

## Build Output 🎉

### Location
```
electron-app/dist/win-unpacked/
```

### Executable
```
SayAs TTS.exe (176 MB)
```

### To Run
Double-click `dist/win-unpacked/SayAs TTS.exe` or run from command line:
```bash
C:\Users\User\.qwen\projects\SayAs\electron-app\dist\win-unpacked\SayAs TTS.exe
```

### Notes
- The unpacked version is fully functional!
- Portable .exe installer build was attempted but NSIS packing was slow
- All features work in the unpacked build

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

### Electron App
```bash
# Development
cd electron-app
.\start.bat

# Run built app
.\dist\win-unpacked\SayAs TTS.exe

# Build installer (requires Admin)
.\build.bat
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
- ✅ Gradio WebUI (pink notebook theme, 4 tabs!)
- ✅ Interactive HTML Dashboard
- ✅ API with Swagger docs
- ✅ **Electron Desktop App** (Windows .exe - BUILT!)

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
│   ├── webui.py        # Gradio UI (4 tabs!)
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
├── electron-app/       # Desktop app
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
f396afa Working Before Build 💕🎮
d9a7312 UI improvements: tabs, API auto-start, keep model loaded 💕
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
- **NEW**: WebUI has 4 tabs including embedded documentation!
- **NEW**: Electron desktop app - BUILT AND WORKING!

---

## Running the Built App

### Option 1: Unpacked Build (READY NOW!)
```bash
C:\Users\User\.qwen\projects\SayAs\electron-app\dist\win-unpacked\SayAs TTS.exe
```

### Option 2: Development Mode
```bash
cd electron-app
.\start.bat
```

### Option 3: Build Installer (requires Admin)
```bash
cd electron-app
.\build.bat
```

---

**--yolo! 💕🎮✨**

*Made with excessive love and way too many features*
