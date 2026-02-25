@echo off
setlocal

REM Set CUDA PATH
set PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin

REM Activate venv and run SayAs WebUI
call "%~dp0venv\Scripts\activate.bat"
echo.
echo ========================================
echo   💕 SayAs WebUI 💕
echo ========================================
echo.
echo 🌸 Opening in your browser...
echo.
python "%~dp0src\webui.py"

endlocal
