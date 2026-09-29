@echo off
title ClaimAI - Flask API
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found.
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"

echo ==========================================
echo          ClaimAI API Server
echo ==========================================
echo.
echo Virtual environment activated.
echo API: http://127.0.0.1:5000/api/health
echo.
echo Press CTRL+C to stop.
echo.

python app.py
pause
