import importlib
import tempfile
import os
import subprocess
import sys
import shutil
import winsound
import threading
from config import TTS_PROVIDER, TTS_VOICE


def _play_wav(wav_path):
    """Play WAV file with fallback options."""
    if not os.path.exists(wav_path):
        return False

    # Method 1: winsound (reliable, built-in)
    try:
        winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_SYNC)
        return True
    except Exception:
        pass

    # Method 2: Windows Media Player via comtypes (if available)
    try:
        from comtypes.client import CreateObject
        player = CreateObject("MediaPlayer.MediaPlayer.7")
        player.URL = os.path.abspath(wav_path)
        player.controls.play()

        # Wait for playback to complete
        import time
        while player.playState == 3:  # 3 = playing
            time.sleep(0.1)
        return True
    except Exception:
        pass

    # Method 3: pygame (if available)
    try:
        import pygame
        pygame.mixer.init()
        sound = pygame.mixer.Sound(wav_path)
        sound.play()
        import time
        time.sleep(sound.get_length())
        return True
    except Exception:
        pass

    return False


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
            timeout=10,  # 10s — достаточно для Edge TTS, избегать зависания
        )

        if result.returncode != 0:
            return False

        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            return False

        return _play_wav(temp_path)
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
    # sys.executable is the Python interpreter path (e.g., .venv/Scripts/python.exe)
    # piper.exe should be in the same directory
    venv_scripts_dir = os.path.dirname(sys.executable)

    piper_paths = [
        os.path.join(venv_scripts_dir, "piper.exe"),  # In venv Scripts
        os.path.join(os.environ.get("ProgramFiles", ""), "piper", "piper.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "piper", "piper.exe"),
    ]

    for path in piper_paths:
        if os.path.exists(path):
            return path

    # Check PATH separately
    path = shutil.which("piper.exe") or shutil.which("piper")
    if path:
        return path

    return None


def _download_piper_voice(voice_name, model_dir=".cache/piper_voices"):
    """Download Piper voice if not already present."""
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)

    voice_file = os.path.join(model_dir, f"{voice_name}.onnx")
    config_file = os.path.join(model_dir, f"{voice_name}.onnx.json")

    if not os.path.exists(voice_file) or not os.path.exists(config_file):
        # Build correct HuggingFace URLs for Piper voices
        urls = _build_piper_urls(voice_name)

        import urllib.request

        for base_url in urls:
            try:
                print(f"[Piper] Trying to download from {base_url}...")
                onnx_url = f"{base_url}.onnx"
                json_url = f"{base_url}.onnx.json"

                urllib.request.urlretrieve(onnx_url, voice_file, reporthook=lambda a, b, c: None)
                print(f"[Piper] Downloaded {voice_name}.onnx ({os.path.getsize(voice_file) / 1024 / 1024:.1f} MB)")

                urllib.request.urlretrieve(json_url, config_file)
                print(f"[Piper] Downloaded {voice_name}.onnx.json")
                return True
            except Exception as e:
                print(f"[Piper] Failed: {e}")
                # Cleanup failed downloads
                try:
                    if os.path.exists(voice_file):
                        os.remove(voice_file)
                    if os.path.exists(config_file):
                        os.remove(config_file)
                except:
                    pass
                continue

        print(f"[Piper] All download URLs failed for voice: {voice_name}")
        return False
    return True


def _build_piper_urls(voice_name: str) -> list:
    """Build correct download URLs for Piper voices on HuggingFace."""
    # Russian voices have a special path structure
    if voice_name.startswith("ru_"):
        base = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/{voice_name}/ruslan/medium/{voice_name}-ruslan-medium"
        return [base]

    # English and other languages — generic fallback
    parts = voice_name.split("_")
    if len(parts) >= 2:
        lang_code = f"{parts[0]}_{parts[1]}"
        base = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{lang_code}/{voice_name}/medium/{voice_name}-medium"
        return [base]

    # Last resort fallback
    return [f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/{voice_name}"]


def _speak_piper(text, voice_name="ru_RU"):
    """Speak text using Piper TTS via Python API."""
    try:
        from piper import PiperVoice
    except ImportError:
        return False

    model_dir = os.path.abspath(".cache/piper_voices")
    os.makedirs(model_dir, exist_ok=True)

    try:
        # Check if voice files exist
        voice_file = os.path.join(model_dir, f"{voice_name}.onnx")
        config_file = os.path.join(model_dir, f"{voice_name}.onnx.json")

        if not os.path.exists(voice_file) or not os.path.exists(config_file):
            print("[Piper] Voice files not found, downloading...")
            # Download voice
            if not _download_piper_voice(voice_name, model_dir):
                return False

        # Load voice from existing files
        voice = PiperVoice.load(voice_name, model_dir)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_path = temp_file.name

        # Synthesize speech to WAV file
        with open(temp_path, "wb") as wav_file:
            voice.synthesize(text, wav_file)

        file_size = os.path.getsize(temp_path) if os.path.exists(temp_path) else 0
        if file_size > 0:
            return _play_wav(temp_path)
        return False
    except Exception as e:
        print(f"[Piper] Error: {e}")
        return False
    finally:
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass


# Lazy, thread-safe pyttsx3 engine initialization
_engine = None
_engine_lock = threading.Lock()
_tts_timeout_seconds = 60.0  # Increased from 10s to 60s for longer texts


def _get_engine():
    """Lazy, thread-safe pyttsx3 engine initialization (double-check locking)."""
    global _engine
    if _engine is None:
        with _engine_lock:
            if _engine is None:
                _engine = _create_engine()
    return _engine


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
    """Fallback TTS using pyttsx3 with lazy engine init."""
    try:
        engine = _get_engine()
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
    import sys
    # Re-import config to get updated value
    import importlib
    importlib.reload(sys.modules.get('config', None))
    from config import TTS_PROVIDER as new_provider
    globals()['TTS_PROVIDER'] = new_provider


def get_tts_provider():
    """Get current TTS provider."""
    return TTS_PROVIDER
