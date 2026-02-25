@echo off
setlocal

REM SayAs Electron App - Development Start
REM =======================================

echo.
echo ========================================
echo   💕 SayAs TTS - Development 💕
echo ========================================
echo.

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo 📦 Installing npm dependencies...
    call npm install
)

echo.
echo 🚀 Starting Electron app...
echo.

call npm start

endlocal
