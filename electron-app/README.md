# SayAs TTS - Electron Desktop App

**LUDICUS OVERKILL Edition** 💕🎮

Beautiful standalone desktop application for SayAs Text-to-Speech.

---

## Quick Start

### Development

```bash
cd electron-app
npm install
npm start
```

### Build Windows Installer

**Note:** Requires Administrator privileges for symbolic link creation.

```bash
# Run as Administrator
npm run build:win
```

The installer will be created in `dist/` folder.

---

## Build Troubleshooting

### "A required privilege is not held by the client"

This error occurs when building without Administrator privileges. Windows requires elevated permissions to create symbolic links during the build process.

**Solution:** Run the build command as Administrator:

1. Open Command Prompt or PowerShell as Administrator
2. Navigate to the electron-app folder
3. Run: `npm run build:win`

### Alternative: Enable Developer Mode

Windows 10/11 Developer Mode allows symlink creation without admin:

1. Settings → Update & Security → For Developers
2. Enable "Developer Mode"
3. Try building again

---

## Features

- 🌸 Standalone Windows executable
- 💕 Pink notebook theme
- 🎤 Custom voice upload
- ✨ Long text auto-splitting
- 🎮 All OVERKILL features included
- 🔊 GPU acceleration support

---

## Project Structure

```
electron-app/
├── src/
│   ├── main/
│   │   └── main.js          # Electron main process
│   ├── preload/
│   │   └── preload.js       # IPC bridge
│   └── renderer/
│       └── index.html       # Loading screen
├── assets/
│   ├── icon.svg             # App icon
│   └── icon.png             # PNG version
├── package.json
└── LICENSE
```

---

## Requirements

### For Development
- Node.js 18+
- npm 9+

### For Running Built App
- Windows 10/11
- NVIDIA GPU with CUDA 11.8 (optional, for GPU acceleration)
- Python 3.11 with dependencies (bundled in installer)

---

## Building the Installer

### 1. Install Dependencies

```bash
npm install
```

### 2. Prepare Python Environment

The installer needs to bundle the Python environment:

```bash
# From project root
xcopy /E /I /Y venv electron-app\python\venv
xcopy /E /I /Y src electron-app\python\src
```

### 3. Build

```bash
npm run build:win
```

### 4. Find Installer

Installer location: `electron-app/dist/SayAs TTS-4.0.0-Setup.exe`

---

## Configuration

### electron-builder (package.json)

```json
{
  "build": {
    "appId": "com.sayas.tts",
    "win": {
      "target": "nsis"
    }
  }
}
```

### Customization

- **Icon**: Replace `assets/icon.ico`
- **Version**: Update `version` in package.json
- **Ports**: Modify in `src/main/main.js`

---

## Troubleshooting

### App Won't Start

1. Check if Python backend is running
2. Verify CUDA installation (if using GPU)
3. Check logs in `%APPDATA%\SayAs TTS\logs\`

### Build Fails

1. Ensure all files in `assets/` exist
2. Check Node.js version (18+)
3. Run `npm install` again

### Voice Upload Not Working

1. Check write permissions to user data folder
2. Verify voices directory exists

---

## License

MIT License - See LICENSE file

---

**Made with 💕 and excessive features** | **--yolo! 💕🎮✨**
