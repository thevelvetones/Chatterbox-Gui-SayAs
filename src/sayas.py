"""
SayAs - Custom Voice TTS CLI using Chatterbox
Usage: SayAs <speaker> "<text>" [-output <filepath>]
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path

# Set CUDA PATH before importing torch
os.environ['PATH'] = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin;' + os.environ.get('PATH', '')

import torch
import torchaudio
import pyaudio
import numpy as np
from chatterbox.tts import ChatterboxTTS

# Project paths
PROJECT_DIR = Path(__file__).parent
VOICES_DIR = PROJECT_DIR / "voices"


def get_device():
    """Get GPU if available, otherwise CPU."""
    if torch.cuda.is_available():
        return "cuda"
    print("WARNING: CUDA not available, using CPU (slower)")
    return "cpu"


def load_model(device: str):
    """Load Chatterbox TTS model."""
    print("Loading Chatterbox TTS model...", file=sys.stderr)
    model = ChatterboxTTS.from_pretrained(device=device)
    return model


def find_voice(speaker: str) -> Path:
    """Find voice sample for speaker."""
    VOICES_DIR.mkdir(exist_ok=True)
    
    # Check for voice file with various extensions
    for ext in ['.wav', '.mp3']:
        voice_path = VOICES_DIR / f"{speaker}{ext}"
        if voice_path.exists():
            return voice_path
    
    # Check if speaker name is a path
    speaker_path = Path(speaker)
    if speaker_path.exists():
        return speaker_path
    
    return None


def generate_speech(model, text: str, voice_path: Path = None, device: str = "cuda"):
    """Generate speech using Chatterbox."""
    if voice_path:
        print(f"Using voice sample: {voice_path}", file=sys.stderr)
        wav = model.generate(text, audio_prompt_path=str(voice_path))
    else:
        print(f"Using default voice for: {text[:50]}...", file=sys.stderr)
        wav = model.generate(text)
    
    return wav


def play_audio(wav: torch.Tensor, sample_rate: int):
    """Play audio using pyaudio."""
    # Convert to numpy and normalize to 16-bit
    audio_data = wav.cpu().numpy().flatten()
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Initialize pyaudio
    p = pyaudio.PyAudio()
    
    try:
        # Open stream
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            output=True
        )
        
        # Play audio
        stream.write(audio_data.tobytes())
        stream.stop_stream()
        stream.close()
    finally:
        p.terminate()


def save_audio(wav: torch.Tensor, sample_rate: int, output_path: str):
    """Save audio to file."""
    torchaudio.save(output_path, wav, sample_rate)
    print(f"Saved audio to: {output_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="SayAs - Text-to-Speech with custom voices",
        usage='SayAs <speaker> "<text>" [-output <filepath>]'
    )
    parser.add_argument("speaker", help="Speaker name or path to voice sample")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("-output", "-o", dest="output", help="Output file path (optional)")
    
    args = parser.parse_args()
    
    # Get device
    device = get_device()
    
    # Load model
    model = load_model(device)
    
    # Find voice
    voice_path = find_voice(args.speaker)
    
    # Generate speech
    wav = generate_speech(model, args.text, voice_path, device)
    
    # Output
    if args.output:
        save_audio(wav, model.sr, args.output)
    else:
        print("Playing audio...", file=sys.stderr)
        play_audio(wav, model.sr)
        print("Done!", file=sys.stderr)


if __name__ == "__main__":
    main()
