@echo off
setlocal

REM Set CUDA PATH
set PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin

REM Activate venv and run SayAs
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0src\sayas.py" %*

endlocal
