@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo [INFO] Installing dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [INFO] Starting JarviX GUI...
".venv\Scripts\python.exe" app_gui.py
if errorlevel 1 (
    echo [ERROR] App closed with an error.
    pause
)

endlocal
