@echo off
:: Local Voice Assistant - Universal Launcher
:: Choose between GUI and CLI voice modes

setlocal enabledelayedexpansion

:: Переход в корневую директорию проекта (scripts/../)
cd /d "%~dp0.."

echo ============================================================
echo  Local Voice Assistant - Launcher
echo ============================================================
echo.
echo Choose mode:
echo   [1] GUI - Graphical Interface (recommended)
echo   [2] CLI - Voice Console (direct commands)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" goto gui_mode
if "%choice%"=="2" goto cli_mode
echo Invalid choice. Exiting.
exit /b 1

:gui_mode
echo.
echo Starting GUI mode...
echo ============================================================
goto setup

:cli_mode
echo.
echo Starting CLI voice mode...
echo ============================================================
echo HOW TO USE:
echo   1. Wait for "Ассистент готов к работе"
echo   2. Speak: "JARVIS, [your question]"
echo   Examples:
echo     - "JARVIS, какое сейчас время?"
echo     - "JARVIS, открой Google"
echo ============================================================
goto setup

:setup
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

:: Start selected application
echo.
if "%choice%"=="1" (
    echo [START] Launching GUI...
    ".venv\Scripts\python.exe" app_gui.py
) else (
    echo [START] Launching CLI voice mode...
    ".venv\Scripts\python.exe" main.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Application closed with an error.
    echo [INFO] Check logs in .logs/ directory for details.
    echo.
    pause
)

endlocal
