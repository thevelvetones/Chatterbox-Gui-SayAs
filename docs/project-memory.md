# SayAs Project Memory

## Project Info
- **Name**: SayAs
- **Base**: Chatterbox TTS (Resemble AI)
- **Location**: C:\Users\User\.qwen\projects\SayAs
- **Status**: Core functionality working --yolo!

## Requirements
- Python 3.11 with GPU support (CUDA 11.8) + CPU fallback
- Chatterbox TTS library
- PyAudio for playback (no VLC/external players)

## Hardware
- **GPU**: NVIDIA GeForce GTX 1050 (2GB VRAM)
- **CUDA**: 11.8 at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`
- **PyTorch**: 2.5.1+cu118

## CLI Interface
```
SayAs <speaker> "<text>" [-output <filepath>]
SayAs <speaker> "<text>" -o <filepath>
```

## Behavior
- Audio plays immediately by default (PyAudio player)
- Audio files (.wav/.mp3) only saved when -output specified
- GPU first, fallback to CPU if needed
- Voice samples stored in `voices/` folder

## Project Structure
```
SayAs/
├── sayas.bat          # CLI launcher (includes CUDA PATH)
├── src/sayas.py       # Main application
├── voices/            # Custom voice samples
├── venv/              # Python virtual environment
├── docs/              # Documentation
├── README.md
└── todo.md
```

## Tested & Working
- [x] GPU inference (GTX 1050)
- [x] CPU fallback
- [x] Default voice TTS
- [x] Audio playback (PyAudio)
- [x] File output (-output flag)
- [x] CLI argument parsing

## Future Plans (NOT YET)
- REST API server (after core functionality confirmed working)
- Speaker management commands
- Batch processing
