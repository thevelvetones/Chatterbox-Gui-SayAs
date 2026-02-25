@echo off
setlocal

REM SayAs Electron App - Build Windows Installer
REM =============================================

echo.
echo ========================================
echo   💕 SayAs TTS - Build Installer 💕
echo ========================================
echo.

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo 📦 Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        exit /b 1
    )
)

REM Copy Python environment
echo.
echo 🐍 Copying Python environment...
if not exist "python" mkdir python

if exist "..\venv" (
    echo    Copying venv...
    xcopy /E /I /Q /Y "..\venv" "python\venv"
) else (
    echo    ⚠️  venv not found - will need manual setup
)

if exist "..\src" (
    echo    Copying src...
    xcopy /E /I /Q /Y "..\src" "python\src"
)

if exist "..\voices" (
    echo    Copying voices...
    xcopy /E /I /Q /Y "..\voices" "voices"
)

if exist "..\presets" (
    echo    Copying presets...
    xcopy /E /I /Q /Y "..\presets" "presets"
)

REM Create placeholder icon if missing
if not exist "assets\icon.png" (
    echo    ⚠️  icon.png not found - using placeholder
    echo    Please add a proper icon for production builds
)

REM Build
echo.
echo 🔨 Building Windows installer...
echo.
call npm run build:win

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo.
    exit /b 1
)

echo.
echo ========================================
echo   ✅ Build Complete! 💕
echo ========================================
echo.
echo 📦 Installer location:
echo    dist\SayAs TTS-4.0.0-Setup.exe
echo.
echo 🎮 Ready to install on Windows!
echo.

endlocal
