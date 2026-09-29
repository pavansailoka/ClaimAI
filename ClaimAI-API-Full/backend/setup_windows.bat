@echo off
title ClaimAI - Virtual Environment Setup
cd /d "%~dp0"

echo ==========================================
echo       ClaimAI Backend Setup
echo ==========================================

where py >nul 2>&1
if %errorlevel% neq 0 (
    echo Python launcher "py" was not found.
    echo Install Python 3.11+ from python.org and enable "Add Python to PATH".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3 -m venv .venv
)

echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Setup complete.
echo Virtual environment: %CD%\.venv
echo.
pause
