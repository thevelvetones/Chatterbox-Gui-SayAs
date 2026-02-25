@echo off
setlocal EnableDelayedExpansion

REM SayAs - List Available Voices

echo ========================================
echo   SayAs - Available Voices
echo ========================================
echo.
echo 🌸 Default Voice (Chatterbox Built-in)
echo.
echo 💕 Custom Voices:

REM Check if voices folder exists
if not exist "voices\" (
    echo.
    echo    No voices/ folder found.
    echo    Add .wav or .mp3 files there to create custom voices!
    goto :footer
)

REM Count and list voices
set count=0
for %%f in (voices\*.wav voices\*.mp3) do (
    if exist "%%f" (
        for %%i in ("%%f") do echo    - %%~ni
        set /a count+=1
    )
)

if !count! == 0 (
    echo.
    echo    No custom voices found.
    echo    Add .wav or .mp3 files to voices/ folder!
) else (
    echo.
    echo    Total: !count! custom voice(s)
)

:footer
echo.
echo ========================================
echo.
echo Usage: SayAs ^<voice^> "^<text^>"
echo Example: SayAs Kate "Hello there!"
echo.

endlocal
