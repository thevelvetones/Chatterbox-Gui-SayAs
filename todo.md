# SayAs - LUDICUS OVERKILL Edition

## Project Overview
CLI + API + WebUI text-to-speech using Chatterbox (Resemble AI) with custom speaker voices, voice morphing, audio effects, batch processing, and EVERYTHING ELSE.

**Status**: COMPLETE --yolo! 🎮✨

## Usage

### CLI
```bash
SayAs Kate "This is what I want Kate to say in Kate Voice"
SayAs Kate "text" -output path\to\file.wav
```

### API (Port 8765)
```bash
POST /sayas - Generate speech with morphing/effects
POST /batch - Batch processing
POST /ssml - SSML-like advanced control
GET  /voices - List voices
GET  /presets - List presets
WS   /stream - WebSocket streaming
```

### WebUI
- **Dashboard**: http://localhost:8765/dashboard.html
- **Gradio UI**: http://localhost:7860
- **API Docs**: http://localhost:8765/docs

## Tasks

### Phase 1: Core Setup ✅
- [x] Create project structure (docs, src, voices/)
- [x] Set up Python virtual environment
- [x] Install Chatterbox TTS dependencies
- [x] Verify GPU availability (CUDA 11.8) with CPU fallback

### Phase 2: Voice Library ✅
- [x] Implement voice sample storage (.wav/.mp3)
- [x] Create speaker registration from voice samples
- [x] Build speaker lookup/retrieval system

### Phase 3: CLI Implementation ✅
- [x] Parse command line arguments (speaker, text, -output)
- [x] Implement TTS generation with selected speaker
- [x] Add immediate audio playback (Python player - no VLC)
- [x] Add optional file output (-output <filepath>)

### Phase 4: Testing ✅
- [x] Test GPU inference (GTX 1050)
- [x] Test CPU fallback
- [x] Test voice playback
- [x] Test file output
- [x] Test multiple speakers

### Phase 5: Documentation ✅
- [x] Setup instructions
- [x] Usage guide
- [x] README.md

### Phase 6: API Server ✅
- [x] REST API endpoint for TTS
- [x] Speaker management via API
- [x] Model persistence in memory
- [x] Multiple output modes (play, return, both, save)

### Phase 7: WebUI ✅
- [x] Beautiful pink notebook-themed Gradio interface
- [x] Interactive HTML dashboard
- [x] Voice selection dropdown
- [x] Real-time audio playback

### Phase 8: LUDICUS OVERKILL Features ✅ 🎮
- [x] Voice Morphing (pitch, speed, volume)
- [x] Audio Effects (reverb, echo, chorus, distortion, normalize)
- [x] Batch Processing
- [x] Voice Presets (save/load)
- [x] SSML-like Markup Support
- [x] Background Music Mixing
- [x] Multiple Output Formats (wav, mp3, flac, ogg)
- [x] WebSocket Streaming
- [x] Health Check Endpoint
- [x] Interactive Control Dashboard

### Phase 9: Future Enhancements (NOT YET - but who knows!)
- [ ] Discord bot integration
- [ ] Real-time voice changing
- [ ] Multi-speaker conversations
- [ ] Audio book generation
- [ ] Cloud deployment

## Notes
- **GPU**: NVIDIA GeForce GTX 1050 (2GB VRAM)
- **CUDA**: 11.8 required
- **PyTorch**: 2.5.1+cu118
- **Python audio player only** (no VLC/external players)
- **Audio files only saved when -output specified** (CLI) or output_mode="save"/"return" (API)
- **All docs in /docs folder as .md files**

## Project Structure
```
SayAs/
├── sayas.bat              # CLI launcher
├── start-api.bat          # API server launcher
├── start-webui.bat        # WebUI launcher
├── dashboard.html         # Interactive control dashboard
├── src/
│   ├── sayas.py           # CLI application
│   ├── api.py             # FastAPI server (OVERKILL edition)
│   └── webui.py           # Gradio WebUI
├── voices/                # Custom voice samples
├── output/                # Generated audio files
├── presets/               # Voice presets
├── venv/                  # Python virtual environment
├── docs/
│   ├── usage.md           # Full usage guide
│   └── project-memory.md  # Project details
├── README.md              # Quick start guide
└── todo.md                # This file!
```

## OVERKILL Features Summary 🎮
1. **Voice Morphing**: Adjust pitch (0.5-2.0x), speed (0.5-2.0x), volume (0-2.0x)
2. **Audio Effects**: Reverb, echo, chorus, distortion, normalization
3. **Batch Processing**: Process multiple texts at once
4. **Voice Presets**: Save and load complete voice configurations
5. **SSML Support**: Advanced markup for segment-by-segment control
6. **Background Music**: Mix music with generated speech
7. **Multiple Formats**: WAV, MP3, FLAC, OGG output
8. **WebSocket Streaming**: Real-time TTS streaming
9. **Interactive Dashboard**: Beautiful control center with all features
10. **Health Monitoring**: API status, GPU info, voice/preset counts

--yolo till you fail or want to talk! 💕🎮✨
