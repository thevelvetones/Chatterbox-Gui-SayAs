@echo off
setlocal

REM SayAs Documentation Static Server
REM Starts a simple HTTP server for viewing docs

cd /d "%~dp0"

echo.
echo ========================================
echo   💕 SayAs Documentation Server 💕
echo ========================================
echo.
echo 📖 Opening docs in your browser...
echo.
echo Server: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start Python HTTP server in background
start "" cmd /c "cd docs && python -m http.server 8080"

REM Wait a moment then open browser
timeout /t 2 /nobreak >nul
start http://localhost:8080

echo.
echo 💖 Documentation server started!
echo.

endlocal
