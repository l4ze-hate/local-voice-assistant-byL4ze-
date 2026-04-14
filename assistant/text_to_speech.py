import importlib
import tempfile
import os
import subprocess
import sys
import winsound
from config import TTS_PROVIDER, TTS_VOICE


def _speak_edge(text):
    """Speak text using Edge TTS with winsound playback."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_path = temp_file.name

    try:
        # Generate audio with edge-tts
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "edge_tts",
                "--voice",
                TTS_VOICE,
                "--text",
                text,
                "--write-media",
                temp_path
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode != 0:
            return False
        
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            return False
        
        try:
            # Use SND_SYNC for synchronous playback (wait for sound to complete)
            winsound.PlaySound(temp_path, winsound.SND_FILENAME | winsound.SND_SYNC)
            return True
        except Exception:
            return False
    except Exception:
        return False
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def _create_engine():
    """Create pyttsx3 engine for fallback TTS."""
    try:
        pyttsx3 = importlib.import_module("pyttsx3")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: pyttsx3. Install with `pip install -r requirements.txt`."
        ) from exc
    return pyttsx3.init()


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


def _download_piper_voice(voice_name, model_dir=".cache/piper_voices"):
    """Download Piper voice if not already present."""
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    voice_file = os.path.join(model_dir, f"{voice_name}.onnx")
    config_file = os.path.join(model_dir, f"{voice_name}.onnx.json")
    
    if not os.path.exists(voice_file) or not os.path.exists(config_file):
        # Download from official Piper repository
        base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/{voice_name}"
        import urllib.request
        
        try:
            urllib.request.urlretrieve(f"{base_url}/{voice_file}", voice_file)
            urllib.request.urlretrieve(f"{base_url}/{config_file}", config_file)
            return True
        except Exception:
            return False
    return True


def _speak_piper(text, voice_name="ru_RU"):
    """Speak text using Piper TTS (offline, no API key required)."""
    piper_exe = _get_piper_path()
    if not piper_exe:
        return False
    
    model_dir = ".cache/piper_voices"
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
            try:
                # Use SND_SYNC for synchronous playback
                winsound.PlaySound(temp_path, winsound.SND_FILENAME | winsound.SND_SYNC)
                return True
            except Exception:
                return False
        return False
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


engine = _create_engine()
_tts_timeout_seconds = 60.0  # Increased from 10s to 60s for longer texts


def speak(text):
    """Speak text using configured TTS provider with fallback chain.
    
    Order: Edge TTS → Piper → pyttsx3
    """
    print("Ассистент: ", text)
    
    # Truncate very long texts to avoid excessive processing time
    if len(text) > 1000:
        text = text[:1000] + "..."
        print("(Text truncated for TTS - too long)")

    # Try providers in order
    providers_to_try = []
    
    # Add primary provider first
    if TTS_PROVIDER.lower() == "edge":
        providers_to_try.append(("edge", _speak_edge))
        providers_to_try.append(("piper", lambda t: _speak_piper(t, TTS_VOICE)))
    elif TTS_PROVIDER.lower() == "piper":
        providers_to_try.append(("piper", lambda t: _speak_piper(t, TTS_VOICE)))
        providers_to_try.append(("edge", _speak_edge))
    
    # Always add pyttsx3 as final fallback
    providers_to_try.append(("pyttsx3", _speak_fallback))
    
    # Try each provider
    for provider_name, provider_func in providers_to_try:
        try:
            if provider_name == "pyttsx3":
                # pyttsx3 doesn't return success indicator
                provider_func(text)
                return
            else:
                if provider_func(text):
                    return
        except Exception:
            continue
    
    # If all providers fail, just print the text
    pass


def _speak_fallback(text):
    """Fallback TTS using pyttsx3."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


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