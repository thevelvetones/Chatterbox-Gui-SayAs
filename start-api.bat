@echo off
setlocal

REM Set CUDA PATH
set PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin

REM Activate venv and run SayAs API Server
call "%~dp0venv\Scripts\activate.bat"
echo.
echo ========================================
echo   💖 SayAs API Server 💖
echo ========================================
echo.
echo 📱 API: http://localhost:8765
echo 📚 Docs: http://localhost:8765/docs
echo 🌸 WebUI: http://localhost:7860
echo.
echo Press Ctrl+C to stop
echo.
python "%~dp0src\api.py"

endlocal
