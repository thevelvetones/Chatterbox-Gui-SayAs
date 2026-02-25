# SayAs - LUDICUS OVERKILL Edition 💕🎮

**The most extra text-to-speech system you never knew you needed!**

SayAs is a powerful TTS (Text-to-Speech) application built on Chatterbox TTS with extensive customization features including voice cloning, voice morphing, audio effects, batch processing, and more.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [CLI Usage](#cli-usage)
- [API Server](#api-server)
- [WebUI](#webui)
- [Dashboard](#dashboard)
- [Voice Morphing](#voice-morphing)
- [Audio Effects](#audio-effects)
- [Batch Processing](#batch-processing)
- [Voice Presets](#voice-presets)
- [SSML-like Control](#ssml-like-control)
- [WebSocket Streaming](#websocket-streaming)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### List Available Voices
```bash
.\listVoices.bat
```

### CLI - Basic Usage
```bash
SayAs Kate "This is what I want Kate to say in Kate Voice"
SayAs Kate "Hello" -output greeting.wav
```

### Start API Server
```bash
.\start-api.bat
# API: http://localhost:8765
# Swagger Docs: http://localhost:8765/docs
```

### Start WebUI
```bash
.\start-webui.bat
# Open: http://localhost:7860
```

### Open Dashboard
Open `dashboard.html` in your browser for the full control center!

---

## Installation

### System Requirements

- **OS**: Windows 10/11
- **Python**: 3.11
- **GPU**: NVIDIA GPU with CUDA 11.8 support (GTX 1050 or better recommended)
- **CUDA Toolkit**: 11.8 at `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`

### Setup Steps

1. **Clone/Navigate to the project:**
   ```bash
   cd C:\Users\User\.qwen\projects\SayAs
   ```

2. **Activate the virtual environment:**
   ```bash
   .\venv\Scripts\activate
   ```

3. **Install dependencies (if needed):**
   ```bash
   pip install chatterbox-tts pyaudio fastapi uvicorn gradio
   ```

4. **Verify installation:**
   ```bash
   .\listVoices.bat
   ```

---

## CLI Usage

### Basic Syntax

```bash
SayAs <speaker> "<text>" [-output <filepath>]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `<speaker>` | Speaker name or path to voice sample file |
| `<text>` | Text to convert to speech (wrap in quotes) |
| `-output, -o` | Optional: Output file path to save audio |
| `-chunk-size` | Max characters per chunk for long text (default: 800) |
| `-silence` | Seconds of silence between chunks (default: 0.5) |
| `-no-split` | Disable automatic long text splitting |

### Long Text Support

When using custom voice samples with text over 900 characters, SayAs automatically:
1. Splits text into chunks at sentence boundaries
2. Processes each chunk separately
3. Stitches audio together with silence gaps

**Example with long text:**
```bash
# Automatic splitting for long text
SayAs Kate "This is a very long text that exceeds the limit..."

# Customize chunk size
SayAs Kate "Long text..." -chunk-size 600

# Customize silence between chunks
SayAs Kate "Long text..." -silence 1.0

# Disable auto-splitting (may cause errors with long text)
SayAs Kate "Long text..." -no-split
```

### Examples

**Using default voice:**
```bash
SayAs Kate "Hello world!"
```

**Using custom voice sample:**
```bash
# Place voice sample in voices/ folder
SayAs Kate "Hello from my custom voice!"
```

**Using direct voice file path:**
```bash
SayAs "C:\path\to\voice.wav" "Text using this voice"
```

**Save to file:**
```bash
SayAs Kate "Welcome message" -output welcome.wav
SayAs John "Goodbye" -o C:\Users\Public\goodbye.mp3
```

---

## API Server

### Starting the Server

```bash
.\start-api.bat
```

**Endpoints:**
- API: http://localhost:8765
- Swagger UI: http://localhost:8765/docs

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and features |
| `/voices` | GET | List available voices |
| `/sayas` | POST | Generate speech with full options |
| `/batch` | POST | Batch process multiple texts |
| `/ssml` | POST | SSML-like advanced segment control |
| `/presets` | GET/POST | List or save voice presets |
| `/presets/{name}` | GET | Load specific preset |
| `/health` | GET | Health check with system info |
| `/stream` | WS | WebSocket streaming |

### Example API Request

```bash
curl -X POST http://localhost:8765/sayas \
  -H "Content-Type: application/json" \
  -d '{
    "voice": "Kate",
    "text": "Hello world!",
    "output_mode": "both",
    "morphing": {
      "pitch": 1.0,
      "speed": 1.0,
      "volume": 1.0
    },
    "effects": {
      "reverb": false,
      "echo": false,
      "chorus": false,
      "distortion": false,
      "normalize": true
    }
  }'
```

### Long Text Handling (API)

The API automatically handles long text (900+ characters) when using custom voices:

```json
{
  "voice": "Kate",
  "text": "This is a very long text that will be automatically split...",
  "output_mode": "return"
}
```

Response includes `long_text_processed: true` if splitting was applied:

```json
{
  "success": true,
  "long_text_processed": true,
  "duration_seconds": 45.2,
  ...
}
```

---

## WebUI

### Starting the WebUI

```bash
.\start-webui.bat
```

Open http://localhost:7860 in your browser.

### Features

- 🌸 Beautiful pink notebook-themed interface
- 💕 Voice selection dropdown (auto-refreshes)
- ✨ Text input with character support
- 🔊 Server-side audio playback option
- 🎵 Audio download capability

---

## Dashboard

Open `dashboard.html` in your browser for the complete control center.

### Dashboard Features

- **Real-time Status**: API status, GPU info, voice/preset counts
- **Quick Speak**: Generate speech with voice selection
- **Voice Morphing**: Adjust pitch, speed, volume in real-time
- **Audio Effects**: Toggle reverb, echo, chorus, distortion
- **Background Music**: Mix background music with speech
- **Voice Presets**: Save and load custom configurations
- **Batch Processing**: Process multiple texts at once
- **Activity Log**: Real-time operation logging

---

## Voice Morphing

Adjust voice characteristics with these parameters:

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| **Pitch** | 0.5 - 2.0 | 1.0 | Voice pitch/frequency |
| **Speed** | 0.5 - 2.0 | 1.0 | Speech rate |
| **Volume** | 0.1 - 2.0 | 1.0 | Output volume |

### Usage Example (API)

```json
{
  "voice": "Kate",
  "text": "Hello!",
  "morphing": {
    "pitch": 1.2,
    "speed": 0.9,
    "volume": 1.1
  }
}
```

---

## Audio Effects

Apply professional audio effects to your generated speech:

| Effect | Description | Additional Parameters |
|--------|-------------|----------------------|
| **Reverb** | Adds room ambiance | `reverb_amount: 0.0-1.0` |
| **Echo** | Adds delay-based echo | `echo_delay: seconds` |
| **Chorus** | Creates chorus effect | `chorus_amount: 0.0-1.0` |
| **Distortion** | Adds harmonic distortion | `distortion_amount: 0.0-1.0` |
| **Normalize** | Normalizes audio levels | - |

### Usage Example

```json
{
  "voice": "Kate",
  "text": "Hello with effects!",
  "effects": {
    "reverb": true,
    "reverb_amount": 0.5,
    "echo": true,
    "echo_delay": 0.4,
    "chorus": false,
    "distortion": false,
    "normalize": true
  }
}
```

---

## Batch Processing

Process multiple text-to-speech requests in a single API call.

### Request Format

```json
POST /batch
{
  "items": [
    {"voice": "Kate", "text": "First line", "morphing": {...}},
    {"voice": "John", "text": "Second line", "morphing": {...}}
  ],
  "output_mode": "save",
  "output_format": "wav"
}
```

### Response

```json
{
  "batch_id": "20250224_143022",
  "total": 2,
  "successful": 2,
  "results": [
    {"index": 0, "success": true, "path": "...", "url": "..."},
    {"index": 1, "success": true, "path": "...", "url": "..."}
  ]
}
```

---

## Voice Presets

Save and load voice configurations for quick access.

### Save a Preset

```json
POST /presets
{
  "name": "My Awesome Preset",
  "voice": "Kate",
  "morphing": {
    "pitch": 1.1,
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

### Load Presets

```bash
GET /presets          # List all presets
GET /presets/{name}   # Get specific preset
```

---

## SSML-like Control

Advanced segment-by-segment control for complex speech generation.

### Request Format

```json
POST /ssml
{
  "segments": [
    {
      "text": "Hello there!",
      "voice": "Kate",
      "pitch": 1.0,
      "speed": 1.0,
      "emotion": "happy"
    },
    {
      "text": "And now in a different voice...",
      "voice": "John",
      "pitch": 0.9,
      "speed": 1.1
    }
  ],
  "output_mode": "return"
}
```

---

## WebSocket Streaming

Real-time TTS streaming via WebSocket.

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8765/stream');

ws.onopen = () => {
  ws.send(JSON.stringify({
    text: "Hello in real-time!",
    voice: "Kate"
  }));
};

ws.onmessage = (event) => {
  // Receive audio data
  const audioBlob = event.data;
};
```

---

## Custom Voices

### Adding Custom Voices

1. Save your voice sample (.wav or .mp3) in the `voices/` folder
2. Name it after the speaker (e.g., `voices/Kate.wav`)
3. Use the speaker name in your commands

### Voice Sample Guidelines

- **Duration**: 10+ seconds for best results
- **Format**: WAV preferred over MP3 for quality
- **Quality**: Clear, noise-free recording
- **Content**: Natural speech with varied phonemes

---

## Output Formats

Supported audio formats:

| Format | Extension | Quality | Size |
|--------|-----------|---------|------|
| WAV | `.wav` | Lossless | Largest |
| MP3 | `.mp3` | Compressed | Small |
| FLAC | `.flac` | Lossless | Medium |
| OGG | `.ogg` | Compressed | Smallest |

---

## Troubleshooting

### CUDA Not Found

**Symptoms**: Using CPU instead of GPU, slow generation

**Solution**:
1. Ensure NVIDIA drivers are installed
2. Install CUDA 11.8 Toolkit at: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`
3. Restart the application

### Audio Playback Issues

**Symptoms**: No sound when playing

**Solution**:
- Check your default audio output device
- Ensure no other application is exclusively using the audio device
- Try saving to file instead of playback

### Voice Quality Issues

**Symptoms**: Poor voice cloning quality

**Solution**:
- Use a longer voice sample (10+ seconds)
- Use WAV format instead of MP3
- Ensure the sample is clear and noise-free
- Match the language of the sample to your text

### API Server Won't Start

**Symptoms**: Port already in use or connection refused

**Solution**:
```bash
# Check if port is in use
netstat -ano | findstr :8765

# Kill the process if needed
taskkill /PID <PID> /F
```

### Model Loading Errors

**Symptoms**: Out of memory or model loading fails

**Solution**:
- Close other GPU-intensive applications
- Ensure you have enough VRAM (2GB+ recommended)
- Try CPU mode by modifying the device setting

---

## Performance Benchmarks

| Hardware | Generation Time (short sentence) |
|----------|----------------------------------|
| GTX 1050 (GPU) | ~3-5 seconds |
| CPU (fallback) | ~10-15 seconds |

---

## Project Structure

```
SayAs/
├── sayas.bat              # CLI launcher
├── listVoices.bat         # List available voices
├── start-api.bat          # Start API server
├── start-webui.bat        # Start Gradio WebUI
├── dashboard.html         # Control dashboard
├── src/
│   ├── sayas.py           # CLI application
│   ├── api.py             # FastAPI server
│   └── webui.py           # Gradio WebUI
├── voices/                # Custom voice samples (.wav, .mp3)
├── output/                # Generated audio files
├── presets/               # Voice preset configurations
├── venv/                  # Python virtual environment
└── docs/                  # Documentation
    ├── usage.md           # This file
    ├── api-reference.md   # Full API documentation
    ├── webui-guide.md     # WebUI guide
    └── project-memory.md  # Project info
```

---

**Made with 💕 and excessive features** | **--yolo! 💕🎮✨**
