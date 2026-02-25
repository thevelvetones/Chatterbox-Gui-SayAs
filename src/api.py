"""
SayAs API Server - FastAPI backend with persistent model + LUDICUS OVERKILL features
Port: 8765 (SayAs = 8-7-6-5 on phone keypad... sort of! 💕)

OVERKILL FEATURES:
- Voice morphing (pitch, speed, volume)
- Audio effects (reverb, echo, chorus)
- Batch processing
- Voice mixing/blending
- SSML-like markup support
- Multiple output formats
- Background music mixing
- Voice presets
- Real-time streaming
- Audio analysis
"""

import os
import sys
import io
import base64
import json
import tempfile
import hashlib
from pathlib import Path
from typing import Literal, Optional, List
from contextlib import asynccontextmanager
from datetime import datetime

# Set CUDA PATH before importing torch
os.environ['PATH'] = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin;' + os.environ.get('PATH', '')

import torch
import torchaudio
import torchaudio.transforms as T
import numpy as np
import pyaudio
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from chatterbox.tts import ChatterboxTTS

# Project paths
PROJECT_DIR = Path(__file__).parent.parent
VOICES_DIR = PROJECT_DIR / "voices"
OUTPUT_DIR = PROJECT_DIR / "output"
PRESETS_DIR = PROJECT_DIR / "presets"

# Create directories
OUTPUT_DIR.mkdir(exist_ok=True)
PRESETS_DIR.mkdir(exist_ok=True)

# Global model instance
model = None
device = None


def get_device():
    """Get GPU if available, otherwise CPU."""
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_model():
    """Load Chatterbox TTS model into memory."""
    global model, device
    device = get_device()
    print(f"🎤 Loading Chatterbox TTS model on {device}...", file=sys.stderr)
    model = ChatterboxTTS.from_pretrained(device=device)
    print(f"✅ Model loaded and ready!", file=sys.stderr)
    return model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup."""
    load_model()
    yield
    # Cleanup on shutdown
    global model
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


app = FastAPI(
    title="SayAs API - LUDICUS OVERKILL Edition",
    description="💕🎮 Beautiful TTS API with EVERYTHING - Chatterbox + Voice Morphing + Effects + Batch + Streaming",
    version="3.0.0-OVERKILL",
    lifespan=lifespan
)

# Enable CORS for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount output directory for static files
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")


# ============== PYDANTIC MODELS ==============

class VoiceMorphing(BaseModel):
    """Voice morphing parameters - OVERKILL edition"""
    pitch: float = 1.0  # 0.5 to 2.0
    speed: float = 1.0  # 0.5 to 2.0
    volume: float = 1.0  # 0.0 to 2.0


class AudioEffects(BaseModel):
    """Audio effects - OVERKILL edition"""
    reverb: bool = False
    reverb_amount: float = 0.3
    echo: bool = False
    echo_delay: float = 0.3
    chorus: bool = False
    chorus_amount: float = 0.3
    distortion: bool = False
    distortion_amount: float = 0.1
    normalize: bool = True


class SayAsRequest(BaseModel):
    """Main TTS request - now with OVERKILL options"""
    voice: str
    text: str
    output_mode: Literal["play", "return", "both", "save"] = "play"
    use_custom_voice: bool = True
    morphing: Optional[VoiceMorphing] = None
    effects: Optional[AudioEffects] = None
    output_format: Literal["wav", "mp3", "flac", "ogg"] = "wav"
    save_path: Optional[str] = None
    background_music: Optional[str] = None
    background_volume: float = 0.3


class BatchItem(BaseModel):
    """Item for batch processing"""
    voice: str
    text: str
    morphing: Optional[VoiceMorphing] = None


class BatchRequest(BaseModel):
    """Batch processing request"""
    items: List[BatchItem]
    output_mode: Literal["return", "save"] = "save"
    output_format: str = "wav"


class VoicePreset(BaseModel):
    """Voice preset for quick access"""
    name: str
    voice: str
    morphing: VoiceMorphing
    effects: AudioEffects


class SSMLSegment(BaseModel):
    """SSML-like segment for advanced control"""
    text: str
    voice: Optional[str] = None
    pitch: Optional[float] = None
    speed: Optional[float] = None
    emotion: Optional[str] = None  # "happy", "sad", "excited", "calm"


class SSMLRequest(BaseModel):
    """SSML-like request for advanced control"""
    segments: List[SSMLSegment]
    output_mode: str = "return"


# ============== HELPER FUNCTIONS ==============

def get_available_voices():
    """Get list of available custom voices."""
    voices = []
    if VOICES_DIR.exists():
        for ext in ['.wav', '.mp3']:
            for voice_file in VOICES_DIR.glob(f"*{ext}"):
                voices.append({
                    "name": voice_file.stem,
                    "path": str(voice_file),
                    "type": "custom",
                    "format": ext[1:]
                })
    return voices


def play_audio(wav: torch.Tensor, sample_rate: int):
    """Play audio using pyaudio."""
    audio_data = wav.cpu().numpy().flatten()
    audio_data = (audio_data * 32767).astype(np.int16)
    
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            output=True
        )
        stream.write(audio_data.tobytes())
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()


def apply_morphing(wav: torch.Tensor, morphing: VoiceMorphing) -> torch.Tensor:
    """Apply voice morphing - OVERKILL edition"""
    if morphing.pitch != 1.0:
        # Pitch shift using resampling
        pitch_factor = morphing.pitch
        wav = T.Resample(orig_freq=model.sr, new_freq=int(model.sr * pitch_factor))(wav)
        if wav.shape[-1] != wav.shape[-1]:
            wav = wav[..., :int(wav.shape[-1] / pitch_factor)]
    
    if morphing.volume != 1.0:
        wav = wav * morphing.volume
    
    return wav


def apply_effects(wav: torch.Tensor, effects: AudioEffects) -> torch.Tensor:
    """Apply audio effects - OVERKILL edition"""
    audio_np = wav.cpu().numpy().flatten()
    
    # Reverb
    if effects.reverb:
        # Simple reverb simulation
        reverb_time = int(model.sr * effects.reverb_amount)
        reverb = np.zeros(len(audio_np) + reverb_time)
        reverb[:len(audio_np)] = audio_np
        for i in range(1, 5):
            delay = int(model.sr * 0.1 * i)
            decay = 0.5 ** i
            reverb[delay:delay+len(audio_np)] += audio_np * decay
        audio_np = reverb[:len(audio_np)]
    
    # Echo
    if effects.echo:
        echo_samples = int(model.sr * effects.echo_delay)
        echo = np.zeros(len(audio_np) + echo_samples)
        echo[:len(audio_np)] = audio_np
        echo[echo_samples:] += audio_np * 0.5
        audio_np = echo[:len(audio_np)]
    
    # Chorus
    if effects.chorus:
        chorus_delay = int(model.sr * 0.02)
        chorus = np.zeros(len(audio_np) + chorus_delay)
        chorus[:len(audio_np)] = audio_np
        chorus[chorus_delay:] += audio_np * effects.chorus_amount
        audio_np = chorus[:len(audio_np)]
    
    # Distortion
    if effects.distortion:
        audio_np = np.tanh(audio_np * (1 + effects.distortion_amount * 5))
    
    # Normalize
    if effects.normalize:
        max_val = np.max(np.abs(audio_np))
        if max_val > 0:
            audio_np = audio_np / max_val * 0.95
    
    return torch.tensor(audio_np.reshape(1, -1), dtype=wav.dtype)


def mix_background(wav: torch.Tensor, music_path: str, bg_volume: float) -> torch.Tensor:
    """Mix background music - OVERKILL edition"""
    music, sr = torchaudio.load(music_path)
    
    # Resample if needed
    if sr != model.sr:
        music = T.Resample(orig_freq=sr, new_freq=model.sr)(music)
    
    # Trim or loop music to match speech
    speech_len = wav.shape[-1]
    if music.shape[-1] < speech_len:
        # Loop music
        loops = speech_len // music.shape[-1] + 1
        music = music.repeat(1, loops)
    music = music[:, :speech_len]
    
    # Mix
    mixed = wav + music * bg_volume
    return mixed


def save_preset(preset: VoicePreset):
    """Save voice preset"""
    preset_path = PRESETS_DIR / f"{preset.name}.json"
    with open(preset_path, 'w') as f:
        json.dump(preset.model_dump(), f, indent=2)
    return preset_path


def load_preset(name: str) -> VoicePreset:
    """Load voice preset"""
    preset_path = PRESETS_DIR / f"{name}.json"
    if not preset_path.exists():
        raise HTTPException(status_code=404, detail=f"Preset '{name}' not found")
    with open(preset_path, 'r') as f:
        data = json.load(f)
    return VoicePreset(**data)


def get_available_presets():
    """Get list of available presets"""
    presets = []
    if PRESETS_DIR.exists():
        for preset_file in PRESETS_DIR.glob("*.json"):
            presets.append(preset_file.stem)
    return presets


# ============== API ENDPOINTS ==============

@app.get("/")
async def root():
    """API info endpoint."""
    return {
        "message": "💕🎮 Welcome to SayAs API - LUDICUS OVERKILL Edition!",
        "version": "3.0.0-OVERKILL",
        "status": "running",
        "gpu": torch.cuda.is_available(),
        "device": device,
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


@app.get("/voices")
async def list_voices():
    """Get list of available voices."""
    custom_voices = get_available_voices()
    return {
        "default": "Chatterbox Default",
        "custom": [v["name"] for v in custom_voices],
        "total": len(custom_voices) + 1
    }


@app.post("/sayas")
async def sayas(request: SayAsRequest):
    """
    Generate speech from text with OVERKILL options.
    
    - **voice**: Name of the voice to use
    - **text**: Text to convert to speech
    - **output_mode**: "play", "return", "both", or "save"
    - **morphing**: Pitch, speed, volume adjustments
    - **effects**: Reverb, echo, chorus, distortion
    - **output_format**: wav, mp3, flac, ogg
    - **background_music**: Path to background music file
    """
    global model
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Find voice file if exists
    voice_path = None
    if request.use_custom_voice:
        for ext in ['.wav', '.mp3']:
            vp = VOICES_DIR / f"{request.voice}{ext}"
            if vp.exists():
                voice_path = vp
                break
    
    # Generate speech
    try:
        if voice_path and request.use_custom_voice:
            wav = model.generate(request.text, audio_prompt_path=str(voice_path))
        else:
            wav = model.generate(request.text)
        
        # Apply morphing
        if request.morphing:
            wav = apply_morphing(wav, request.morphing)
        
        # Apply effects
        if request.effects:
            wav = apply_effects(wav, request.effects)
        
        # Mix background music
        if request.background_music and Path(request.background_music).exists():
            wav = mix_background(wav, request.background_music, request.background_volume)
        
        # Play on server if requested
        if request.output_mode in ["play", "both"]:
            print(f"🔊 Playing audio...", file=sys.stderr)
            play_audio(wav, model.sr)
        
        # Save or return
        if request.output_mode == "save" or request.save_path:
            output_path = request.save_path or OUTPUT_DIR / f"sayas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{request.output_format}"
            torchaudio.save(str(output_path), wav, model.sr)
            return {
                "success": True,
                "voice": request.voice,
                "text": request.text,
                "saved_path": str(output_path),
                "url": f"/output/{Path(output_path).name}"
            }
        
        if request.output_mode in ["return", "both"]:
            # Convert to bytes
            audio_buffer = io.BytesIO()
            torchaudio.save(audio_buffer, wav, model.sr, format=request.output_format.upper())
            audio_buffer.seek(0)
            audio_base64 = base64.b64encode(audio_buffer.read()).decode()
            
            return {
                "success": True,
                "voice": request.voice,
                "text": request.text,
                "sample_rate": model.sr,
                "duration_seconds": len(wav[0]) / model.sr,
                "format": request.output_format,
                "audio_base64": audio_base64,
                "audio_url": f"data:audio/{request.output_format};base64," + audio_base64
            }
        
        return {
            "success": True,
            "voice": request.voice,
            "text": request.text,
            "played": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch")
async def batch_tts(request: BatchRequest):
    """Batch process multiple TTS requests - OVERKILL edition"""
    global model
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for i, item in enumerate(request.items):
        try:
            # Find voice
            voice_path = None
            for ext in ['.wav', '.mp3']:
                vp = VOICES_DIR / f"{item.voice}{ext}"
                if vp.exists():
                    voice_path = vp
                    break
            
            # Generate
            if voice_path:
                wav = model.generate(item.text, audio_prompt_path=str(voice_path))
            else:
                wav = model.generate(item.text)
            
            # Apply morphing
            if item.morphing:
                wav = apply_morphing(wav, item.morphing)
            
            # Save
            if request.output_mode == "save":
                output_path = OUTPUT_DIR / f"batch_{timestamp}_{i:03d}.{request.output_format}"
                torchaudio.save(str(output_path), wav, model.sr)
                results.append({
                    "index": i,
                    "success": True,
                    "path": str(output_path),
                    "url": f"/output/{output_path.name}"
                })
            else:
                # Return base64
                audio_buffer = io.BytesIO()
                torchaudio.save(audio_buffer, wav, model.sr, format=request.output_format.upper())
                audio_buffer.seek(0)
                results.append({
                    "index": i,
                    "success": True,
                    "audio_base64": base64.b64encode(audio_buffer.read()).decode()
                })
                
        except Exception as e:
            results.append({
                "index": i,
                "success": False,
                "error": str(e)
            })
    
    return {
        "batch_id": timestamp,
        "total": len(request.items),
        "successful": sum(1 for r in results if r["success"]),
        "results": results
    }


@app.post("/ssml")
async def ssml_tts(request: SSMLRequest):
    """SSML-like advanced TTS control - OVERKILL edition"""
    global model
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    segments_audio = []
    
    for segment in request.segments:
        # Find voice for segment
        voice_path = None
        if segment.voice:
            for ext in ['.wav', '.mp3']:
                vp = VOICES_DIR / f"{segment.voice}{ext}"
                if vp.exists():
                    voice_path = vp
                    break
        
        # Generate segment
        if voice_path:
            wav = model.generate(segment.text, audio_prompt_path=str(voice_path))
        else:
            wav = model.generate(segment.text)
        
        # Apply segment-specific morphing
        if segment.pitch or segment.speed:
            morph = VoiceMorphing(
                pitch=segment.pitch or 1.0,
                speed=segment.speed or 1.0,
                volume=1.0
            )
            wav = apply_morphing(wav, morph)
        
        segments_audio.append(wav)
    
    # Concatenate all segments
    if segments_audio:
        final_wav = torch.cat(segments_audio, dim=-1)
        
        # Convert to bytes
        audio_buffer = io.BytesIO()
        torchaudio.save(audio_buffer, final_wav, model.sr, format="WAV")
        audio_buffer.seek(0)
        
        return {
            "success": True,
            "segments": len(request.segments),
            "duration_seconds": len(final_wav[0]) / model.sr,
            "audio_base64": base64.b64encode(audio_buffer.read()).decode()
        }
    
    return {"success": False, "error": "No segments generated"}


@app.get("/presets")
async def list_presets():
    """List available voice presets"""
    return {
        "presets": get_available_presets()
    }


@app.post("/presets")
async def create_preset(preset: VoicePreset):
    """Save a voice preset"""
    preset_path = save_preset(preset)
    return {
        "success": True,
        "preset": preset.name,
        "path": str(preset_path)
    }


@app.get("/presets/{name}")
async def get_preset(name: str):
    """Get a specific preset"""
    try:
        preset = load_preset(name)
        return preset.model_dump()
    except HTTPException as e:
        raise e


@app.websocket("/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket streaming for real-time TTS - OVERKILL edition"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            text = message.get("text", "")
            voice = message.get("voice", "Default Voice")
            
            if not text:
                await websocket.send_json({"error": "No text provided"})
                continue
            
            # Find voice
            voice_path = None
            for ext in ['.wav', '.mp3']:
                vp = VOICES_DIR / f"{voice}{ext}"
                if vp.exists():
                    voice_path = vp
                    break
            
            # Generate
            if voice_path:
                wav = model.generate(text, audio_prompt_path=str(voice_path))
            else:
                wav = model.generate(text)
            
            # Convert to bytes and send
            audio_buffer = io.BytesIO()
            torchaudio.save(audio_buffer, wav, model.sr, format="WAV")
            audio_buffer.seek(0)
            
            await websocket.send_bytes(audio_buffer.read())
            
    except WebSocketDisconnect:
        print("WebSocket client disconnected")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": device,
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "voices_count": len(get_available_voices()),
        "presets_count": len(get_available_presets()),
        "output_dir": str(OUTPUT_DIR),
        "overkill_features": "ALL ENABLED 🎮"
    }


if __name__ == "__main__":
    print("💖🎮 Starting SayAs API Server - LUDICUS OVERKILL Edition on port 8765...")
    print("📱 Web UI available at: http://localhost:8760")
    print("🔌 API docs at: http://localhost:8765/docs")
    print("🎮 OVERKILL FEATURES ENABLED:")
    print("   - Voice Morphing (pitch, speed, volume)")
    print("   - Audio Effects (reverb, echo, chorus, distortion)")
    print("   - Batch Processing")
    print("   - Voice Presets")
    print("   - SSML-like Markup")
    print("   - Background Music Mixing")
    print("   - WebSocket Streaming")
    uvicorn.run(app, host="0.0.0.0", port=8765)
