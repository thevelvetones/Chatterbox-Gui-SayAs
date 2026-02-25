# SayAs - Custom Voice TTS CLI

## Project Overview
CLI tool for text-to-speech using Chatterbox (Resemble AI) with custom speaker voices from saved voice samples.

**Status**: Core functionality COMPLETE --yolo!

## Usage
```
SayAs Kate "This is what I want Kate to say in Kate Voice"
SayAs Kate "text" -output path\to\file.wav
```

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

### Phase 6: Future - API Server (NOT YET)
- [ ] REST API endpoint for TTS
- [ ] Speaker management via API
- [ ] Streaming audio response

### Phase 7: Future Enhancements (NOT YET)
- [ ] Speaker management CLI commands
- [ ] Batch processing
- [ ] Voice sample recording

## Notes
- GPU: NVIDIA GeForce GTX 1050 (2GB VRAM)
- CUDA 11.8 required
- PyTorch 2.5.1+cu118
- Python audio player only (no VLC/external players)
- Audio files only saved when -output specified
- All docs in /docs folder as .md files
