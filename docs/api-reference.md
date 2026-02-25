# SayAs API Reference

**Complete API documentation for SayAs - LUDICUS OVERKILL Edition**

Base URL: `http://localhost:8765`

---

## Table of Contents

- [Overview](#overview)
- [Endpoints](#endpoints)
  - [GET /](#get-)
  - [GET /voices](#get-voices)
  - [POST /sayas](#post-sayas)
  - [POST /batch](#post-batch)
  - [POST /ssml](#post-ssml)
  - [GET /presets](#get-presets)
  - [POST /presets](#post-presets)
  - [GET /presets/{name}](#get-presetsname)
  - [GET /health](#get-health)
  - [WS /stream](#ws-stream)
- [Data Models](#data-models)
- [Error Handling](#error-handling)

---

## Overview

The SayAs API provides a RESTful interface for text-to-speech generation with advanced features including voice morphing, audio effects, batch processing, and real-time streaming.

**Swagger UI**: http://localhost:8765/docs

---

## Endpoints

### GET /

API information and feature overview.

**Response:**
```json
{
  "message": "💕🎮 Welcome to SayAs API - LUDICUS OVERKILL Edition!",
  "version": "3.0.0-OVERKILL",
  "status": "running",
  "gpu": true,
  "device": "cuda",
  "features": [
    "Voice Morphing (pitch, speed, volume)",
    "Audio Effects (reverb, echo, chorus, distortion)",
    "Batch Processing",
    "Voice Presets",
    "SSML-like Markup",
    "Background Music Mixing",
    "Multiple Output Formats",
    "WebSocket Streaming"
  ],
  "endpoints": {
    "GET /voices": "List available voices",
    "POST /sayas": "Generate speech with OVERKILL options",
    "POST /batch": "Batch process multiple texts",
    "POST /ssml": "SSML-like advanced control",
    "GET /presets": "List voice presets",
    "POST /presets": "Save voice preset",
    "GET /presets/{name}": "Load voice preset",
    "GET /health": "Health check",
    "WS /stream": "WebSocket streaming"
  }
}
```

---

### GET /voices

List all available voices (default + custom).

**Response:**
```json
{
  "default": "Chatterbox Default",
  "custom": ["Kate", "John", "Alice"],
  "total": 4
}
```

---

### POST /sayas

Generate speech from text with full OVERKILL options.

**Request Body:**
```json
{
  "voice": "Kate",
  "text": "Hello world!",
  "output_mode": "both",
  "use_custom_voice": true,
  "morphing": {
    "pitch": 1.0,
    "speed": 1.0,
    "volume": 1.0
  },
  "effects": {
    "reverb": false,
    "reverb_amount": 0.3,
    "echo": false,
    "echo_delay": 0.3,
    "chorus": false,
    "chorus_amount": 0.3,
    "distortion": false,
    "distortion_amount": 0.1,
    "normalize": true
  },
  "output_format": "wav",
  "save_path": null,
  "background_music": null,
  "background_volume": 0.3
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `voice` | string | Yes | Voice name or speaker ID |
| `text` | string | Yes | Text to convert to speech |
| `output_mode` | string | No | `"play"`, `"return"`, `"both"`, `"save"` |
| `use_custom_voice` | boolean | No | Use custom voice if available (default: true) |
| `morphing` | object | No | Voice morphing settings |
| `effects` | object | No | Audio effects settings |
| `output_format` | string | No | `"wav"`, `"mp3"`, `"flac"`, `"ogg"` |
| `save_path` | string | No | Custom save path (for `save` mode) |
| `background_music` | string | No | Path to background music file |
| `background_volume` | float | No | Background music volume (0.0-1.0) |

**Output Modes:**

| Mode | Description |
|------|-------------|
| `play` | Play on server speakers only |
| `return` | Return audio as base64 (no playback) |
| `both` | Play AND return as base64 |
| `save` | Save to file (use `save_path` or default) |

**Response (return/both mode):**
```json
{
  "success": true,
  "voice": "Kate",
  "text": "Hello world!",
  "sample_rate": 22050,
  "duration_seconds": 2.5,
  "format": "wav",
  "audio_base64": "UklGRi...",
  "audio_url": "data:audio/wav;base64,UklGRi..."
}
```

**Response (save mode):**
```json
{
  "success": true,
  "voice": "Kate",
  "text": "Hello world!",
  "saved_path": "C:\\...\\output\\sayas_20250224_143022.wav",
  "url": "/output/sayas_20250224_143022.wav"
}
```

**Response (play mode):**
```json
{
  "success": true,
  "voice": "Kate",
  "text": "Hello world!",
  "played": true
}
```

**Error Response:**
```json
{
  "detail": "Model not loaded"
}
```

---

### POST /batch

Batch process multiple TTS requests.

**Request Body:**
```json
{
  "items": [
    {
      "voice": "Kate",
      "text": "First line",
      "morphing": {
        "pitch": 1.0,
        "speed": 1.0,
        "volume": 1.0
      }
    },
    {
      "voice": "John",
      "text": "Second line",
      "morphing": {
        "pitch": 0.9,
        "speed": 1.1,
        "volume": 1.0
      }
    }
  ],
  "output_mode": "save",
  "output_format": "wav"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `items` | array | Yes | Array of batch items |
| `output_mode` | string | No | `"return"` or `"save"` |
| `output_format` | string | No | Output format for all items |

**BatchItem Schema:**
```json
{
  "voice": "Kate",
  "text": "Text to speak",
  "morphing": {
    "pitch": 1.0,
    "speed": 1.0,
    "volume": 1.0
  }
}
```

**Response:**
```json
{
  "batch_id": "20250224_143022",
  "total": 2,
  "successful": 2,
  "results": [
    {
      "index": 0,
      "success": true,
      "path": "C:\\...\\output\\batch_20250224_143022_000.wav",
      "url": "/output/batch_20250224_143022_000.wav"
    },
    {
      "index": 1,
      "success": true,
      "path": "C:\\...\\output\\batch_20250224_143022_001.wav",
      "url": "/output/batch_20250224_143022_001.wav"
    }
  ]
}
```

---

### POST /ssml

SSML-like advanced segment control for complex speech generation.

**Request Body:**
```json
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
      "text": "Now in a different voice...",
      "voice": "John",
      "pitch": 0.9,
      "speed": 1.1,
      "emotion": null
    }
  ],
  "output_mode": "return"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `segments` | array | Yes | Array of speech segments |
| `output_mode` | string | No | `"return"` or `"save"` |

**SSMLSegment Schema:**
```json
{
  "text": "Hello!",
  "voice": "Kate",
  "pitch": 1.0,
  "speed": 1.0,
  "emotion": "happy"
}
```

**Response:**
```json
{
  "success": true,
  "segments": 2,
  "duration_seconds": 5.2,
  "audio_base64": "UklGRi..."
}
```

---

### GET /presets

List all available voice presets.

**Response:**
```json
{
  "presets": ["My Awesome Preset", "Radio Voice", "Storyteller"]
}
```

---

### POST /presets

Save a new voice preset.

**Request Body:**
```json
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
    "reverb_amount": 0.3,
    "echo": false,
    "echo_delay": 0.3,
    "chorus": false,
    "chorus_amount": 0.3,
    "distortion": false,
    "distortion_amount": 0.1,
    "normalize": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "preset": "My Awesome Preset",
  "path": "C:\\...\\presets\\My Awesome Preset.json"
}
```

---

### GET /presets/{name}

Load a specific voice preset.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Preset name (URL-encoded if contains spaces) |

**Example:**
```
GET /presets/My%20Awesome%20Preset
```

**Response:**
```json
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
    "reverb_amount": 0.3,
    "echo": false,
    "echo_delay": 0.3,
    "chorus": false,
    "chorus_amount": 0.3,
    "distortion": false,
    "distortion_amount": 0.1,
    "normalize": true
  }
}
```

**Error Response (404):**
```json
{
  "detail": "Preset 'My Awesome Preset' not found"
}
```

---

### GET /health

Health check with system information.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "gpu_available": true,
  "gpu_name": "NVIDIA GeForce GTX 1050",
  "voices_count": 3,
  "presets_count": 2,
  "output_dir": "C:\\Users\\User\\.qwen\\projects\\SayAs\\output",
  "overkill_features": "ALL ENABLED 🎮"
}
```

---

### WS /stream

WebSocket endpoint for real-time TTS streaming.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8765/stream');
```

**Send Message:**
```json
{
  "text": "Hello in real-time!",
  "voice": "Kate"
}
```

**Receive:**
- Binary audio data (WAV format)

**Error Response:**
```json
{
  "error": "No text provided"
}
```

**Example Client:**
```javascript
const ws = new WebSocket('ws://localhost:8765/stream');

ws.onopen = () => {
  console.log('Connected to TTS stream');
  
  // Send text for synthesis
  ws.send(JSON.stringify({
    text: "Hello world!",
    voice: "Kate"
  }));
};

ws.onmessage = (event) => {
  // Receive binary audio data
  const audioBlob = new Blob([event.data], { type: 'audio/wav' });
  const audioUrl = URL.createObjectURL(audioBlob);
  const audio = new Audio(audioUrl);
  audio.play();
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Connection closed');
};
```

---

## Data Models

### VoiceMorphing

Voice characteristic adjustments.

```json
{
  "pitch": 1.0,      // Range: 0.5 - 2.0
  "speed": 1.0,      // Range: 0.5 - 2.0
  "volume": 1.0      // Range: 0.0 - 2.0
}
```

### AudioEffects

Audio effect parameters.

```json
{
  "reverb": false,           // Enable reverb
  "reverb_amount": 0.3,      // Range: 0.0 - 1.0
  "echo": false,             // Enable echo
  "echo_delay": 0.3,         // Delay in seconds
  "chorus": false,           // Enable chorus
  "chorus_amount": 0.3,      // Range: 0.0 - 1.0
  "distortion": false,       // Enable distortion
  "distortion_amount": 0.1,  // Range: 0.0 - 1.0
  "normalize": true          // Normalize output
}
```

### VoicePreset

Complete voice configuration preset.

```json
{
  "name": "Preset Name",
  "voice": "Kate",
  "morphing": { ... },
  "effects": { ... }
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (preset, voice, etc.) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (model not loaded) |

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Model not loaded` | Server still initializing | Wait for model to load, check /health |
| `Preset '{name}' not found` | Preset doesn't exist | Check preset name, create preset first |
| `No text provided` | Empty text in request | Provide non-empty text string |

---

## Rate Limiting

Currently no rate limiting is implemented. The API processes requests sequentially.

---

## CORS

CORS is enabled for all origins to support web UI access.

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

---

**API Version**: 3.0.0-OVERKILL

**Made with 💕🎮**
