@echo off
:: Build Script - Create standalone .exe files using PyInstaller
:: This script packages the voice assistant into portable executables

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================================
echo  Local Voice Assistant - Build Script
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
                echo [ERROR] Failed to create virtual environment.
                echo [INFO] Python not found in PATH. Please do one of the following:
                echo [INFO] 1. Install Python from https://www.python.org/downloads/
                echo [INFO]    (Check 'Add Python to PATH' during installation)
                echo [INFO] 2. Or run:  "C:\Path\To\Python\python.exe" -m venv .venv
                echo.
                echo [INFO] Trying to find Python in common locations...
                for %%P in (
                    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
                    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
                    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
                    "C:\Python312\python.exe"
                    "C:\Python311\python.exe"
                    "C:\Program Files\Python312\python.exe"
                    "C:\Program Files\Python311\python.exe"
                ) do (
                    if exist "%%~P" (
                        echo [INFO] Found Python at: %%~P
                        "%%~P" -m venv .venv
                        if not errorlevel 1 (
                            echo [OK] Virtual environment created with: %%~P
                            goto venv_created
                        )
                    )
                )
                echo [ERROR] No Python installation found. Please install Python first.
                pause
                exit /b 1
            )
        )
    )
    echo [OK] Virtual environment created
)
:venv_created

:: Install build requirements
echo [SETUP] Installing build dependencies...
".venv\Scripts\python.exe" -m pip install -q pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)

:: Install application requirements
echo [SETUP] Installing application dependencies...
".venv\Scripts\python.exe" -m pip install -q --prefer-binary --only-binary ":all:" -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some packages failed binary install, retrying without --only-binary...
    ".venv\Scripts\python.exe" -m pip install -q --prefer-binary -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)

:: Install Piper TTS
echo [SETUP] Installing Piper TTS...
".venv\Scripts\python.exe" -m pip install -q piper-tts
if errorlevel 1 (
    echo [WARNING] Piper TTS installation had issues, but continuing...
)

:: Clean previous builds
if exist "dist" (
    echo [CLEAN] Removing previous build...
    rmdir /s /q dist
)

:: Build CLI version
echo.
echo [BUILD] Building CLI executable (JarvisCLI.exe)...
echo ============================================================
".venv\Scripts\pyinstaller.exe" ^
    --name "JarvisCLI" ^
    --onefile ^
    --console ^
    --icon=assistant.ico 2>nul ^
    --hidden-import=groq ^
    --hidden-import=edge_tts ^
    --hidden-import=speech_recognition ^
    --hidden-import=sounddevice ^
    --hidden-import=numpy ^
    --hidden-import=piper ^
    --add-data ".env.example;." ^
    --add-data "config.py;." ^
    --add-data "assistant;assistant" ^
    main.py

if errorlevel 1 (
    echo [ERROR] Failed to build CLI executable.
    pause
    exit /b 1
)

:: Build GUI version
echo.
echo [BUILD] Building GUI executable (JarvisGUI.exe)...
echo ============================================================
".venv\Scripts\pyinstaller.exe" ^
    --name "JarvisGUI" ^
    --onefile ^
    --windowed ^
    --icon=assistant.ico 2>nul ^
    --hidden-import=groq ^
    --hidden-import=edge_tts ^
    --hidden-import=speech_recognition ^
    --hidden-import=sounddevice ^
    --hidden-import=numpy ^
    --hidden-import=piper ^
    --hidden-import=customtkinter ^
    --add-data ".env.example;." ^
    --add-data "config.py;." ^
    --add-data "assistant;assistant" ^
    app_gui.py

if errorlevel 1 (
    echo [ERROR] Failed to build GUI executable.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  BUILD COMPLETE!
echo ============================================================
echo.
echo Executables created:
echo   - dist\JarvisCLI.exe  (Command-line voice assistant)
echo   - dist\JarvisGUI.exe  (Graphical interface version)
echo.
echo To use:
echo   1. Copy the .exe file to your desired location
echo   2. Create a .env file with your Groq API key
echo   3. Run the .exe file
echo.
echo API Key: Get free key from https://console.groq.com/keys
echo.
echo ============================================================

endlocal
