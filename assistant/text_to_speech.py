import importlib
import threading
import tempfile
import os
import subprocess
import sys
import winsound
from config import TTS_PROVIDER, TTS_VOICE


def _create_engine():
    try:
        pyttsx3 = importlib.import_module("pyttsx3")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: pyttsx3. Install with `pip install -r requirements.txt`."
        ) from exc
    return pyttsx3.init()

def _speak_edge(text):
    importlib.import_module("edge_tts")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "edge_tts",
                "--voice",
                TTS_VOICE,
                "--text",
                text,
                "--write-media",
                temp_path,
                "--format",
                "riff-24khz-16bit-mono-pcm",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        winsound.PlaySound(temp_path, winsound.SND_FILENAME)
        return True
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def _get_piper_path():
    """Get Piper executable path."""
    # Check if piper is installed
    piper_paths = [
        os.path.join(os.environ.get("ProgramFiles", ""), "piper", "piper.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "piper", "piper.exe"),
        "piper.exe",  # If in PATH
    ]
    
    for path in piper_paths:
        if os.path.exists(path) or path == "piper.exe":
            return path
    return None


def _download_piper_voice(voice_name, model_dir="piper_voices"):
    """Download Piper voice if not already present."""
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    voice_file = os.path.join(model_dir, f"{voice_name}.onnx")
    config_file = os.path.join(model_dir, f"{voice_name}.onnx.json")
    
    if not os.path.exists(voice_file) or not os.path.exists(config_file):
        print(f"Downloading Piper voice: {voice_name}")
        # Download from official Piper repository
        base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/{voice_name}"
        import urllib.request
        
        try:
            urllib.request.urlretrieve(f"{base_url}/{voice_file}", voice_file)
            urllib.request.urlretrieve(f"{base_url}/{config_file}", config_file)
            print(f"Voice downloaded: {voice_name}")
            return True
        except Exception as e:
            print(f"Failed to download voice: {e}")
            return False
    return True


def _speak_piper(text, voice_name="ru_RU"):
    """Speak text using Piper TTS."""
    piper_exe = _get_piper_path()
    if not piper_exe:
        print("Piper TTS: piper.exe not found. Install Piper first.")
        return False
    
    model_dir = "piper_voices"
    if not _download_piper_voice(voice_name, model_dir):
        return False
    
    voice_file = os.path.join(model_dir, f"{voice_name}.onnx")
    config_file = os.path.join(model_dir, f"{voice_name}.onnx.json")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name

    try:
        # Run Piper TTS
        cmd = [
            piper_exe,
            "-m", voice_file,
            "-c", config_file,
            "-f", temp_path,
        ]
        
        process = subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
        )
        
        if process.returncode == 0 and os.path.exists(temp_path):
            winsound.PlaySound(temp_path, winsound.SND_FILENAME)
            return True
        return False
    except subprocess.TimeoutExpired:
        print("Piper TTS timeout")
        return False
    except Exception as e:
        print(f"Piper TTS error: {e}")
        return False
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


engine = _create_engine()
_tts_timeout_seconds = 10.0


def speak(text):
    print("Ассистент: ", text)

    def _speak_primary():
        if TTS_PROVIDER.lower() == "edge":
            return _speak_edge(text)
        elif TTS_PROVIDER.lower() == "piper":
            return _speak_piper(text, TTS_VOICE)
        return False

    def _speak_fallback():
        engine.say(text)
        engine.runAndWait()

    result = {"ok": False}
    errors = []

    def _run():
        try:
            result["ok"] = _speak_primary()
        except Exception as exc:
            errors.append(exc)

        if result["ok"]:
            return

        try:
            _speak_fallback()
            result["ok"] = True
        except Exception as exc:
            errors.append(exc)

    worker = threading.Thread(target=_run, daemon=True)
    worker.start()
    worker.join(_tts_timeout_seconds)

    if worker.is_alive():
        print("TTS timeout. Skipping this phrase to keep assistant responsive.")
    elif not result["ok"] and errors:
        print(f"TTS error: {errors[-1]}")


def set_tts_provider(provider):
    """Change TTS provider at runtime."""
    global TTS_PROVIDER
    import config
    config.TTS_PROVIDER = provider
    # Also update module-level variable
    import builtins
    import sys
    # Re-import config to get updated value
    import importlib
    importlib.reload(sys.modules.get('config', None))
    from config import TTS_PROVIDER as new_provider
    globals()['TTS_PROVIDER'] = new_provider


def get_tts_provider():
    """Get current TTS provider."""
    return TTS_PROVIDER