# SayAs - Custom Voice TTS CLI

Text-to-speech command-line tool using Chatterbox TTS with custom voice support.

## Requirements

- NVIDIA GPU with CUDA 11.8 support (or CPU fallback)
- Python 3.11
- Windows 10/11

## Installation

The project comes with a pre-configured virtual environment. If you need to reinstall:

```bash
cd C:\Users\User\.qwen\projects\SayAs
.\venv\Scripts\activate
pip install chatterbox-tts pyaudio
```

## Usage

### Basic Usage (Default Voice)

```bash
SayAs <speaker_name> "Text to speak"
```

Examples:
```bash
SayAs Kate "This is what I want Kate to say in Kate Voice"
SayAs John "Hello world"
```

### Save to File

```bash
SayAs <speaker_name> "Text to speak" -output <filepath>
SayAs <speaker_name> "Text to speak" -o <filepath>
```

Examples:
```bash
SayAs Kate "Hello there" -output greeting.wav
SayAs John "Welcome" -o C:\Users\Public\welcome.mp3
```

### Using Custom Voice Samples

1. Save a voice sample (.wav or .mp3) in the `voices/` folder
2. Name it after the speaker (e.g., `voices/Kate.wav`)
3. Use the speaker name in the command:

```bash
SayAs Kate "This will use the Kate.wav voice sample"
```

You can also provide a direct path to a voice sample:

```bash
SayAs "C:\path\to\voice.wav" "Text using this voice"
```

## How It Works

1. **Default Voice**: If no voice sample exists for the speaker, Chatterbox uses its default voice
2. **Voice Cloning**: If a voice sample exists in `voices/`, the TTS clones that voice
3. **Audio Output**: 
   - By default, audio plays immediately through your speakers
   - Use `-output` to save to a file instead

## GPU Acceleration

The application automatically uses your NVIDIA GPU (GTX 1050 or better) for faster inference. If CUDA is not available, it falls back to CPU (slower).

## Project Structure

```
SayAs/
├── sayas.bat          # CLI launcher
├── src/
│   └── sayas.py       # Main application
├── voices/            # Custom voice samples (.wav, .mp3)
├── venv/              # Python virtual environment
├── docs/              # Documentation
│   ├── project-memory.md
│   └── usage.md
└── todo.md            # Project tasks
```

## Performance

- **GPU (GTX 1050)**: ~3-5 seconds per short sentence
- **CPU**: ~10-15 seconds per short sentence

## Troubleshooting

### CUDA Not Found
Ensure you have:
- NVIDIA driver installed
- CUDA 11.8 Toolkit installed at: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`

### Audio Playback Issues
- Check your default audio output device
- Ensure no other application is独占 using the audio device

### Voice Quality
- For best voice cloning, use a 10+ second clear voice sample
- WAV format preferred over MP3 for quality

## Future Features (Not Yet Implemented)

- REST API server for remote TTS requests
- Speaker management CLI commands
- Batch processing
- Multiple language support
