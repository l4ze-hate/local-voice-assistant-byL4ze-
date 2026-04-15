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
    python -m venv .venv 2>nul
    if errorlevel 1 (
        py -3 -m venv .venv 2>nul
        if errorlevel 1 (
            py -m venv .venv 2>nul
            if errorlevel 1 (
                echo [ERROR] Python not found. Trying common locations...
                for %%P in (
                    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
                    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
                    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
                    "C:\Python312\python.exe"
                    "C:\Python311\python.exe"
                ) do (
                    if exist "%%~P" (
                        "%%~P" -m venv .venv
                        if not errorlevel 1 (
                            echo [OK] Virtual environment created
                            goto cli_venv_ok
                        )
                    )
                )
                echo [ERROR] No Python found. Install from https://www.python.org/downloads/
                pause
                exit /b 1
            )
        )
    )
    echo [OK] Virtual environment created
)
:cli_venv_ok

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
