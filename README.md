# SayAs

Custom voice text-to-speech CLI using Chatterbox TTS.

## Quick Start

```bash
SayAs Kate "This is what I want Kate to say in Kate Voice"
```

## Install

```bash
cd C:\Users\User\.qwen\projects\SayAs
.\venv\Scripts\activate
pip install chatterbox-tts pyaudio
```

## Usage

| Command | Description |
|---------|-------------|
| `SayAs <speaker> "<text>"` | Speak text with default or cloned voice |
| `SayAs <speaker> "<text>" -output file.wav` | Save to file |
| `SayAs <speaker> "<text>" -o file.wav` | Short form of -output |

## Voice Samples

Place `.wav` or `.mp3` files in `voices/` folder named after the speaker:
- `voices/Kate.wav` → `SayAs Kate "text"`

## Hardware

- **GPU**: NVIDIA GTX 1050 or better (CUDA 11.8)
- **CPU**: Fallback mode (slower)

## Full Documentation

See [docs/usage.md](docs/usage.md) for complete documentation.
