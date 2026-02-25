"""
SayAs - Custom Voice TTS CLI using Chatterbox
Usage: SayAs <speaker> "<text>" [-output <filepath>]

Supports long text automatic splitting for voice cloning.
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

from text_splitter import split_text, stitch_audio_segments, DEFAULT_MAX_CHUNK_SIZE

# Project paths
PROJECT_DIR = Path(__file__).parent
VOICES_DIR = PROJECT_DIR / "voices"

# Long text handling threshold (characters)
LONG_TEXT_THRESHOLD = 900  # Start splitting before hitting the limit


def get_device():
    """Get GPU if available, otherwise CPU."""
    if torch.cuda.is_available():
        return "cuda"
    print("WARNING: CUDA not available, using CPU (slower)", file=sys.stderr)
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


def generate_speech_long_text(
    model,
    text: str,
    voice_path: Path = None,
    device: str = "cuda",
    chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
    silence_duration: float = 0.5
):
    """
    Generate speech for long text by splitting into chunks and stitching.
    
    Args:
        model: ChatterboxTTS model
        text: Long text to convert
        voice_path: Optional path to voice sample
        device: CUDA or CPU
        chunk_size: Maximum characters per chunk
        silence_duration: Seconds of silence between chunks
        
    Returns:
        Combined audio tensor
    """
    print(f"📝 Long text detected ({len(text)} chars), splitting into chunks...", file=sys.stderr)
    
    # Split text
    chunks = split_text(text, max_chunk_size=chunk_size)
    print(f"✂️  Split into {len(chunks)} chunks", file=sys.stderr)
    
    # Generate audio for each chunk
    segments = []
    for i, chunk in enumerate(chunks, 1):
        print(f"🎤 Processing chunk {i}/{len(chunks)} ({len(chunk)} chars)...", file=sys.stderr)
        
        if voice_path:
            wav = model.generate(chunk, audio_prompt_path=str(voice_path))
        else:
            wav = model.generate(chunk)
        
        segments.append(wav)
    
    # Stitch together with silence
    print(f"🔗 Stitching {len(segments)} segments with {silence_duration}s silence...", file=sys.stderr)
    combined = stitch_audio_segments(segments, model.sr, silence_duration)
    
    total_chars = sum(len(c) for c in chunks)
    duration = len(combined[0]) / model.sr
    print(f"✅ Generated {duration:.2f}s of audio from {total_chars} characters", file=sys.stderr)
    
    return combined


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
        description="SayAs - Text-to-Speech with custom voices and long text support",
        usage='SayAs <speaker> "<text>" [-output <filepath>]'
    )
    parser.add_argument("speaker", help="Speaker name or path to voice sample")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("-output", "-o", dest="output", help="Output file path (optional)")
    parser.add_argument(
        "-chunk-size",
        dest="chunk_size",
        type=int,
        default=DEFAULT_MAX_CHUNK_SIZE,
        help=f"Max characters per chunk for long text (default: {DEFAULT_MAX_CHUNK_SIZE})"
    )
    parser.add_argument(
        "-silence",
        dest="silence",
        type=float,
        default=0.5,
        help="Seconds of silence between chunks (default: 0.5)"
    )
    parser.add_argument(
        "-no-split",
        dest="no_split",
        action="store_true",
        help="Disable automatic long text splitting (may cause errors)"
    )

    args = parser.parse_args()

    # Get device
    device = get_device()

    # Load model
    model = load_model(device)

    # Find voice
    voice_path = find_voice(args.speaker)

    # Check if we need to split long text
    needs_split = (
        len(args.text) > LONG_TEXT_THRESHOLD and
        voice_path is not None and  # Only split when using custom voice
        not args.no_split
    )

    # Generate speech
    if needs_split:
        wav = generate_speech_long_text(
            model,
            args.text,
            voice_path,
            device,
            chunk_size=args.chunk_size,
            silence_duration=args.silence
        )
    else:
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
