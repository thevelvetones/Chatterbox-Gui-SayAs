# SayAs WebUI Guide

**Beautiful pink notebook-themed interface for SayAs TTS**

---

## Quick Start

### Starting the WebUI

```bash
.\start-webui.bat
```

Then open **http://localhost:7860** in your browser.

---

## Interface Overview

The WebUI features a beautiful pink notebook theme with:

- 🌸 **Notebook paper effect** - Lined paper background aesthetic
- 💕 **Pink gradient colors** - Feminine, warm color scheme
- ✨ **Dancing Script font** - Elegant cursive headings
- 💖 **Heart animations** - Subtle heartbeat animations
- 🎵 **Clean layout** - Intuitive, easy-to-use interface

---

## Using the WebUI

### 1. Select a Voice

Choose from the **💕 Choose Your Voice** dropdown:

- **🌸 Default Voice** - Chatterbox built-in voice
- **💕 [Voice Name]** - Custom voices from your `voices/` folder

The voice list automatically refreshes when you add new voice samples!

### 2. Enter Your Text

Type your message in the **✨ What should I say?** text box.

- Supports multi-line text
- Maximum 10 lines visible (scrollable)
- No strict character limit

### 3. Choose Playback Options

Check **🔊 Play on server speakers** to:
- Hear the audio immediately through your system speakers
- Uncheck if you only want to download the file

### 4. Generate Speech

Click **💖 Speak It! 💖** to generate speech.

### 5. View Results

- **📝 Status** - Shows success/error messages and duration
- **🎵 Your Audio** - Audio player with download button

---

## Features

### Voice Selection

The dropdown automatically populates with:
- Default Chatterbox voice
- All `.wav` and `.mp3` files in the `voices/` folder

**Adding Custom Voices:**
1. Place your voice sample in `voices/` folder
2. Name it (e.g., `Kate.wav`, `John.mp3`)
3. Refresh the page or restart WebUI
4. Your voice appears in the dropdown!

### Server Playback

When **🔊 Play on server speakers** is checked:
- Audio plays through the server's default output device
- Uses PyAudio for real-time playback
- Perfect for local testing

### Audio Download

Every generation creates a downloadable file:
- Click the download button on the audio player
- File is saved as `temp_output.wav`
- Format: WAV, 22050 Hz sample rate

---

## Screenshots

### Main Interface

```
┌─────────────────────────────────────────────┐
│  💕 SayAs - Beautiful TTS                  │
│  Your beautiful text-to-speech companion   │
├─────────────────────────────────────────────┤
│                                             │
│  💕 Choose Your Voice: [🌸 Default Voice ▼]│
│                                             │
│  ✨ What should I say?                      │
│  ┌─────────────────────────────────────┐   │
│  │ Type your message here, darling...  │   │
│  │                                     │   │
│  │                                     │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ☑ 🔊 Play on server speakers               │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      💖 Speak It! 💖                │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📝 Status: ✅ Success! Generated 2.5s     │
│                                             │
│  🎵 Your Audio                              │
│  ┌─────────────────────────────────────┐   │
│  │ [▶] [━━━━━━●━━━━━━] [🔊] [⬇️]      │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Customization

### CSS Theme Variables

The WebUI uses custom CSS for the pink notebook theme:

```css
/* Background gradient */
background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 50%, #f48fb1 100%);

/* Primary pink */
#ec407a

/* Dark pink */
#d81b60

/* Light pink */
#f48fb1

/* Text color */
#880e4f
```

### Fonts

- **Headings**: Dancing Script (Google Fonts)
- **Body**: Nunito (Google Fonts)

### Notebook Effect

The interface features:
- Vertical pink margin line (like notebook paper)
- Horizontal light pink lines (ruled paper effect)
- Fixed position, non-interactive

---

## Tips & Tricks

### Best Practices

1. **Voice Samples**: Use 10+ second clear recordings for best cloning
2. **Text Length**: Keep messages under 500 characters for quick generation
3. **Playback**: Uncheck server playback if running remotely
4. **Browser**: Works best in Chrome, Firefox, Edge

### Keyboard Shortcuts

- **Ctrl+Enter**: Trigger Speak button (if focused in textarea)

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No voices in dropdown | Add .wav/.mp3 files to `voices/` folder |
| Audio won't play | Check server audio output device |
| Download fails | Check browser download permissions |
| Page won't load | Ensure API server is running |

---

## Technical Details

### Backend

- **Framework**: Gradio
- **Model**: Chatterbox TTS
- **Device**: Auto-detect GPU (CUDA) or CPU fallback

### Audio Pipeline

```
Text Input
    ↓
Chatterbox TTS Model
    ↓
Voice Cloning (if custom voice)
    ↓
Waveform Generation
    ↓
PyAudio Playback (optional)
    ↓
Save to temp_output.wav
    ↓
Gradio Audio Player
```

### File Locations

| File | Purpose |
|------|---------|
| `src/webui.py` | WebUI source code |
| `temp_output.wav` | Temporary audio file |
| `voices/` | Custom voice samples |

---

## Comparison: WebUI vs Dashboard

| Feature | WebUI (Gradio) | Dashboard (HTML) |
|---------|----------------|------------------|
| **Theme** | Pink notebook | Pink notebook |
| **Voice Morphing** | ❌ | ✅ |
| **Audio Effects** | ❌ | ✅ |
| **Batch Processing** | ❌ | ✅ |
| **Presets** | ❌ | ✅ |
| **API Status** | ❌ | ✅ |
| **Simplicity** | ✅✅✅ | ✅ |
| **Quick TTS** | ✅✅✅ | ✅✅ |

**Use WebUI when**: You want simple, quick TTS generation
**Use Dashboard when**: You need advanced features and control

---

## Starting Options

### Default Launch
```bash
.\start-webui.bat
```

### Manual Launch with Options
```bash
python src/webui.py
```

### Programmatic Launch
```python
from webui import main
main()
```

---

## Integration

### Embed in Other Pages

The WebUI can be embedded via iframe:

```html
<iframe src="http://localhost:7860" width="100%" height="800"></iframe>
```

### Share Link

For remote access, modify `webui.py`:
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=True,  # Creates public shareable link
)
```

---

## Known Limitations

1. **No Voice Morphing**: Use Dashboard for pitch/speed/volume control
2. **No Effects**: Use Dashboard for reverb, echo, chorus, etc.
3. **Single Generation**: One request at a time
4. **No Presets**: Can't save/load configurations

---

## Future Enhancements

Potential future features:
- [ ] Built-in voice morphing controls
- [ ] Audio effects toggles
- [ ] Batch processing interface
- [ ] Preset management
- [ ] Real-time voice preview
- [ ] SSML editor
- [ ] History of generated speech

---

**Made with 💕 and Gradio** | **SayAs v3.0-OVERKILL**
