"""
SayAs WebUI - Beautiful pink notebook-themed interface
Built with Gradio

Features:
- Text-to-speech with custom voices
- Voice upload and management
- Pink notebook theme
"""

import os
import sys
import io
import shutil
from pathlib import Path

# Set CUDA PATH before importing torch
os.environ['PATH'] = r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin;' + os.environ.get('PATH', '')

import torch
import torchaudio
import numpy as np
import pyaudio
import gradio as gr

from chatterbox.tts import ChatterboxTTS

# Project paths
PROJECT_DIR = Path(__file__).parent.parent
VOICES_DIR = PROJECT_DIR / "voices"

# Ensure voices directory exists
VOICES_DIR.mkdir(exist_ok=True)

# Global model
model = None
device = None


def get_device():
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_model():
    global model, device
    device = get_device()
    print(f"🎤 Loading Chatterbox TTS model on {device}...")
    model = ChatterboxTTS.from_pretrained(device=device)
    print(f"✅ Model loaded!")
    return model


def get_available_voices():
    """Get list of available voices for dropdown."""
    voices = ["🌸 Default Voice"]
    if VOICES_DIR.exists():
        for ext in ['.wav', '.mp3']:
            for voice_file in VOICES_DIR.glob(f"*{ext}"):
                voices.append(f"💕 {voice_file.stem}")
    return voices


def get_voices_list():
    """Get simple list of voice names for display."""
    voices = []
    if VOICES_DIR.exists():
        for ext in ['.wav', '.mp3']:
            for voice_file in VOICES_DIR.glob(f"*{ext}"):
                voices.append(f"💕 {voice_file.stem} ({voice_file.suffix})")
    if not voices:
        voices = ["📭 No custom voices yet - upload one!"]
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


def generate_speech(voice_name, text, play_on_server):
    """Generate speech from text."""
    global model

    if model is None:
        return "❌ Model not loaded yet. Please wait...", None

    if not text.strip():
        return "⚠️ Please enter some text to speak!", None

    # Clean voice name (handle list or string)
    if isinstance(voice_name, list):
        voice_name = voice_name[0] if voice_name else "Default Voice"
    if voice_name is None:
        voice_name = "Default Voice"

    voice = str(voice_name).replace("🌸 ", "").replace("💕 ", "")

    # Find voice file
    voice_path = None
    if voice != "Default Voice":
        for ext in ['.wav', '.mp3']:
            vp = VOICES_DIR / f"{voice}{ext}"
            if vp.exists():
                voice_path = vp
                break

    try:
        # Generate speech
        if voice_path:
            print(f"🎵 Using custom voice: {voice}")
            wav = model.generate(text, audio_prompt_path=str(voice_path))
        else:
            print(f"🎵 Using default voice")
            wav = model.generate(text)

        # Play on server
        if play_on_server:
            print("🔊 Playing audio...")
            play_audio(wav, model.sr)

        # Save to temp file for Gradio
        output_path = PROJECT_DIR / "temp_output.wav"
        torchaudio.save(str(output_path), wav, model.sr)

        duration = len(wav[0]) / model.sr
        status = f"✅ Success! Generated {duration:.2f}s of speech with {'custom' if voice_path else 'default'} voice"

        return status, str(output_path)

    except Exception as e:
        return f"❌ Error: {str(e)}", None


def upload_voice(voice_name, audio_file):
    """
    Upload and save a new voice sample.
    
    Args:
        voice_name: Name for the voice
        audio_file: Path to uploaded audio file
        
    Returns:
        Status message and updated voices list
    """
    if not voice_name or not voice_name.strip():
        return "⚠️ Please enter a voice name!", get_voices_list()
    
    if audio_file is None:
        return "⚠️ Please select an audio file!", get_voices_list()
    
    # Clean the voice name
    voice_name = voice_name.strip()
    voice_name = "".join(c for c in voice_name if c.isalnum() or c in (' ', '-', '_'))
    
    if not voice_name:
        return "⚠️ Invalid voice name!", get_voices_list()
    
    try:
        # Determine file extension from uploaded file
        file_ext = Path(audio_file).suffix.lower()
        if file_ext not in ['.wav', '.mp3']:
            # Convert to wav if not supported
            file_ext = '.wav'
        
        # Create destination path
        dest_path = VOICES_DIR / f"{voice_name}{file_ext}"
        
        # Copy the file
        shutil.copy2(audio_file, dest_path)
        
        print(f"💾 Voice saved: {voice_name}{file_ext}")
        
        return f"✅ Voice '{voice_name}' saved successfully!", get_voices_list()
    
    except Exception as e:
        return f"❌ Error saving voice: {str(e)}", get_voices_list()


def delete_voice(voice_name):
    """Delete a voice sample."""
    if not voice_name or "Default" in voice_name or "No custom" in voice_name:
        return "⚠️ Cannot delete this voice!", get_voices_list()
    
    # Clean voice name
    voice = str(voice_name).replace("💕 ", "").split(" ")[0]
    
    try:
        deleted = False
        for ext in ['.wav', '.mp3']:
            voice_path = VOICES_DIR / f"{voice}{ext}"
            if voice_path.exists():
                voice_path.unlink()
                deleted = True
                break
        
        if deleted:
            print(f"🗑️ Voice deleted: {voice}")
            return f"✅ Voice '{voice}' deleted!", get_voices_list()
        else:
            return "⚠️ Voice not found!", get_voices_list()
    
    except Exception as e:
        return f"❌ Error deleting voice: {str(e)}", get_voices_list()


# Custom CSS for pink notebook theme
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Nunito:wght@400;600;700&display=swap');

.gradio-container {
    background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 50%, #f48fb1 100%);
    font-family: 'Nunito', sans-serif;
    min-height: 100vh;
}

/* Notebook paper effect */
.gradio-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 60px;
    width: 3px;
    height: 100%;
    background: linear-gradient(to bottom, #e91e63 0%, #e91e63 100%);
    opacity: 0.3;
    z-index: -1;
}

.gradio-container::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
        repeating-linear-gradient(
            transparent,
            transparent 31px,
            rgba(233, 30, 99, 0.1) 32px
        );
    pointer-events: none;
    z-index: -1;
}

/* Header styling */
header {
    background: linear-gradient(135deg, #ec407a 0%, #d81b60 100%);
    border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(233, 30, 99, 0.3) !important;
    border: 3px solid #fff !important;
    margin: 20px !important;
    padding: 30px !important;
}

header h1 {
    font-family: 'Dancing Script', cursive !important;
    font-size: 3.5em !important;
    color: white !important;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.3) !important;
}

/* Input boxes */
textarea, input[type="text"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px dashed #ec407a !important;
    border-radius: 15px !important;
    font-family: 'Nunito', sans-serif !important;
}

/* Buttons */
button.primary {
    background: linear-gradient(135deg, #ec407a 0%, #d81b60 100%) !important;
    border: none !important;
    border-radius: 25px !important;
    font-family: 'Dancing Script', cursive !important;
    font-size: 1.3em !important;
    box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4) !important;
    transition: all 0.3s ease !important;
}

button.primary:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(233, 30, 99, 0.5) !important;
}

/* Secondary button */
button.secondary {
    background: linear-gradient(135deg, #f48fb1 0%, #ec407a 100%) !important;
}

/* Danger button */
button.danger {
    background: linear-gradient(135deg, #ef5350 0%, #d32f2f 100%) !important;
}

/* Dropdown */
select {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #f48fb1 !important;
    border-radius: 15px !important;
}

/* Status box */
#status-box {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 3px solid #ec407a !important;
    border-radius: 20px !important;
    font-size: 1.1em !important;
}

/* Audio player */
audio {
    border-radius: 15px !important;
    border: 3px solid #f48fb1 !important;
}

/* Footer */
footer {
    text-align: center;
    color: #880e4f;
    font-size: 0.9em;
    margin-top: 20px;
}

/* Checkbox */
input[type="checkbox"] {
    accent-color: #ec407a;
}

/* Label */
label {
    color: #880e4f !important;
    font-weight: 600 !important;
}

/* Voice list */
.voice-list {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
}
"""

# Create the interface
with gr.Blocks(css=custom_css, title="💕 SayAs - Beautiful TTS") as demo:

    gr.HTML("""
        <div style="text-align: center; margin-bottom: 10px;">
            <span style="font-size: 2em;">💖</span>
            <span style="font-size: 2em;">✨</span>
            <span style="font-size: 2em;">💕</span>
        </div>
    """)

    # Main TTS Section
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
                ## 🌸 Welcome to SayAs!

                *Your beautiful text-to-speech companion*

                ### How to use:
                1. 💕 Pick a voice from the dropdown
                2. ✨ Type your message
                3. 🎵 Click "Speak It!" to hear it
                4. 💖 Download if you want to save it

                ---

                **💡 Tip:** Upload your own voice samples below!
            """)

            with gr.Group():
                gr.HTML("""
                    <div style="text-align: center; font-size: 1.5em; margin: 10px;">
                        💗 Made with love 💗
                    </div>
                """)

        with gr.Column(scale=2):
            voice_dropdown = gr.Dropdown(
                choices=["🌸 Default Voice"],
                value="🌸 Default Voice",
                label="💕 Choose Your Voice",
                interactive=True
            )

            text_input = gr.Textbox(
                label="✨ What should I say?",
                placeholder="Type your message here, darling...",
                lines=4,
                max_lines=10
            )

            play_checkbox = gr.Checkbox(
                label="🔊 Play on server speakers",
                value=True
            )

            speak_button = gr.Button(
                "💖 Speak It! 💖",
                variant="primary",
                size="lg"
            )

            status_output = gr.Textbox(
                label="📝 Status",
                interactive=False,
                elem_id="status-box"
            )

            audio_output = gr.Audio(
                label="🎵 Your Audio",
                type="filepath"
            )

    gr.HTML("""
        <hr style="border: 2px dashed #ec407a; margin: 30px 0;">
    """)

    # Voice Management Section
    gr.Markdown("""
        ## 🎤 Voice Management
        
        Upload your own voice samples (.wav or .mp3) to create custom voices!
        
        **Tips for best results:**
        - Use clear, high-quality recordings (10+ seconds)
        - WAV format preferred over MP3
        - Name your voice something memorable
    """)

    with gr.Row():
        # Upload Section
        with gr.Column(scale=1):
            gr.Markdown("### ➕ Add New Voice")
            
            voice_name_input = gr.Textbox(
                label="🏷️ Voice Name",
                placeholder="e.g., Kate, John, MyVoice",
                interactive=True
            )
            
            voice_file_upload = gr.File(
                label="📁 Upload Audio File",
                file_types=[".wav", ".mp3"],
                interactive=True
            )
            
            upload_button = gr.Button(
                "💾 Save Voice",
                variant="primary",
                size="lg"
            )
            
            upload_status = gr.Textbox(
                label="📝 Upload Status",
                interactive=False,
                elem_id="status-box"
            )

        # Voice List Section
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Existing Voices")
            
            voices_list_display = gr.List(
                label="Your Voices",
                value=[["📭 No custom voices yet - upload one!"]],
                interactive=False
            )
            
            with gr.Row():
                voice_to_delete = gr.Dropdown(
                    choices=[],
                    label="🗑️ Select Voice to Delete",
                    interactive=True
                )
                
                delete_button = gr.Button(
                    "❌ Delete",
                    variant="stop",
                    size="lg"
                )
            
            delete_status = gr.Textbox(
                label="📝 Delete Status",
                interactive=False
            )

    gr.HTML("""
        <footer>
            <p>💕 SayAs v3.0 - Powered by Chatterbox TTS 💕</p>
            <p>✨ GPU Accelerated | 🎵 Custom Voices | 💖 Voice Upload | 🎮 OVERKILL Features</p>
        </footer>
    """)

    # Event handlers
    speak_button.click(
        fn=generate_speech,
        inputs=[voice_dropdown, text_input, play_checkbox],
        outputs=[status_output, audio_output]
    )

    # Voice upload
    upload_button.click(
        fn=upload_voice,
        inputs=[voice_name_input, voice_file_upload],
        outputs=[upload_status, voices_list_display]
    )

    # Voice delete
    delete_button.click(
        fn=delete_voice,
        inputs=[voice_to_delete],
        outputs=[delete_status, voices_list_display]
    )

    # Refresh voice dropdown on page load
    demo.load(
        fn=get_available_voices,
        outputs=[voice_dropdown]
    )
    
    # Also refresh the voices list and delete dropdown
    def refresh_voice_lists():
        voices = get_voices_list()
        delete_choices = [v for v in voices if "Default" not in v and "No custom" not in v]
        return voices, delete_choices
    
    # Initial load
    demo.load(
        fn=refresh_voice_lists,
        outputs=[voices_list_display, voice_to_delete]
    )
    
    # Refresh after upload
    upload_button.click(
        fn=refresh_voice_lists,
        outputs=[voices_list_display, voice_to_delete]
    )
    
    # Refresh after delete
    delete_button.click(
        fn=refresh_voice_lists,
        outputs=[voices_list_display, voice_to_delete]
    )


def main():
    print("💖 Loading model...")
    load_model()

    print("💕 Starting SayAs WebUI...")
    print("🌸 Open http://localhost:7860 in your browser!")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
