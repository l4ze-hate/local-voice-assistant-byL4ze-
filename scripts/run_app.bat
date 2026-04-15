@echo off
:: Local Voice Assistant - GUI Launcher
:: This script sets up and runs the voice assistant with full GUI

setlocal enabledelayedexpansion

:: Переход в корневую директорию проекта (scripts/../)
cd /d "%~dp0.."

echo ============================================================
echo  Local Voice Assistant - Starting...
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
                            goto app_venv_ok
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
:app_venv_ok

:: Install base requirements
echo [SETUP] Installing Python packages...
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: Install Piper TTS (required for voice)
echo [SETUP] Installing Piper TTS (voice synthesis)...
".venv\Scripts\python.exe" -m pip install -q piper-tts
if errorlevel 1 (
    echo [WARNING] Piper TTS installation had issues, but continuing...
)

:: Check for .env file
if not exist ".env" (
    echo.
    echo [WARNING] .env file not found!
    echo [INFO] Creating .env file template...
    (
        echo # Local Voice Assistant Configuration
        echo GROQ_API_KEY=gsk_your_api_key_here
        echo AI_PROVIDER=groq
        echo TTS_PROVIDER=piper
    ) > .env
    echo [INFO] IMPORTANT: Edit .env and add your Groq API key from https://console.groq.com/keys
    echo.
    pause
)

:: Verify setup
echo [SETUP] Verifying system setup...
".venv\Scripts\python.exe" verify_setup.py 2>nul
if errorlevel 1 (
    echo [WARNING] Some systems may not be configured correctly.
    echo.
)

:: Start GUI application
echo.
echo [START] Launching Voice Assistant GUI...
echo ============================================================
echo.
".venv\Scripts\python.exe" app_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application closed with an error.
    echo [INFO] Check logs in .logs/ directory for details.
    echo.
    pause
)

endlocal
