@echo off
:: Local Voice Assistant - CLI Voice Mode
:: This script runs the voice assistant in command-line mode
:: Just speak your commands with "JARVIS" wake word!

setlocal enabledelayedexpansion

:: Переход в корневую директорию проекта (scripts/../)
cd /d "%~dp0.."

echo ============================================================
echo  Local Voice Assistant - CLI MODE
echo ============================================================
echo.

:: Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Creating virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

:: Install base requirements
echo [SETUP] Installing Python packages...
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: Install Piper TTS
echo [SETUP] Installing Piper TTS...
".venv\Scripts\python.exe" -m pip install -q piper-tts

:: Check .env
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo [INFO] Creating .env file...
    (
        echo # Local Voice Assistant Configuration
        echo GROQ_API_KEY=gsk_your_api_key_here
    ) > .env
    echo [ERROR] STOP: Add your Groq API key to .env file
    echo Get key from: https://console.groq.com/keys
    echo.
    pause
    exit /b 1
)

:: Start CLI
echo.
echo ============================================================
echo HOW TO USE:
echo   1. Wait for "Ассистент готов к работе" (ready message)
echo   2. Speak: "JARVIS, [your question]"
echo   Examples:
echo     - "JARVIS, какое сейчас время?"
echo     - "JARVIS, расскажи про Python"
echo     - "JARVIS, открой Google"
echo ============================================================
echo.
echo [START] Starting Voice Assistant (CLI mode)...
".venv\Scripts\python.exe" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application error
    pause
)

endlocal
