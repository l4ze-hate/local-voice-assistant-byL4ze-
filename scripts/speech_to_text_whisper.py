#!/usr/bin/env python
"""
Speech-to-text using OpenAI Whisper API
This module provides speech recognition using OpenAI's Whisper API
which handles low-level audio signals much better than Google STT.

SETUP:
1. Install: pip install openai
2. Get API key: https://platform.openai.com/api-keys
3. Set OPENAI_API_KEY env var or add to key.env:
   OPENAI_API_KEY=sk-proj-your-key-here
"""

import os
import tempfile
import sounddevice
import numpy as np
from config import LANGUAGE

# Try to import whisper-capable clients
openai_client = None
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    pass

def get_microphone_names():
    """Get list of available microphones."""
    try:
        import sounddevice
        devices = sounddevice.query_devices()
        names = []
        for i, device in enumerate(devices):
            if device.get("max_input_channels", 0) > 0:
                names.append(f"[{i}] {device.get('name', f'Input {i}')}")
        return names
    except:
        return []

def record_audio_with_sounddevice(duration=5, sample_rate=16000, device_index=None):
    """Record audio using sounddevice.
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Sample rate (16000 Hz is standard for speech)
        device_index: Microphone device index (None = system default)
    
    Returns:
        numpy array of audio data or None if error
    """
    try:
        print(f"Recording {duration} seconds of audio...")
        audio_data = sounddevice.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16',
            device=device_index
        )
        sounddevice.wait()
        print(f"Recording complete: {audio_data.shape}")
        return audio_data
    except Exception as e:
        print(f"Failed to record audio: {e}")
        return None

def amplify_audio(audio_data, target_level=0.8):
    """Amplify audio to prevent clipping while maximizing signal.
    
    Args:
        audio_data: numpy array of int16 audio
        target_level: Target level (0-1)
    
    Returns:
        normalized numpy array
    """
    # Convert to float for processing
    audio_float = audio_data.astype(np.float32) / 32768.0
    
    # Find max amplitude
    max_amplitude = max(abs(audio_float.min()), abs(audio_float.max()))
    
    if max_amplitude > 0:
        # Scale to target level
        scale = (target_level / max_amplitude)
        audio_float = audio_float * scale
        # Clip to prevent overflow
        audio_float = np.clip(audio_float, -1.0, 1.0)
    
    # Convert back to int16
    return (audio_float * 32767).astype(np.int16)

def listen_whisper(duration=5, device_index=None):
    """Listen to microphone and transcribe using OpenAI Whisper API.
    
    Args:
        duration: Recording duration in seconds
        device_index: Microphone device index
    
    Returns:
        Transcribed text or empty string if failed
    """
    if openai_client is None:
        print("ERROR: OpenAI client not initialized.")
        print("Install: pip install openai")
        print("Get key: https://platform.openai.com/api-keys")
        print("Set: OPENAI_API_KEY=sk-proj-...")
        return ""
    
    # Record audio
    audio_data = record_audio_with_sounddevice(duration, device_index=device_index)
    if audio_data is None:
        return ""
    
    # Amplify if needed
    audio_data = amplify_audio(audio_data)
    
    # Save to temporary WAV file
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            import wave
            wav_file = f.name
            with wave.open(wav_file, 'wb') as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(16000)
                wav.writeframes(audio_data.tobytes())
        
        # Transcribe with Whisper API
        print(f"Sending to Whisper API for transcription...")
        with open(wav_file, 'rb') as f:
            response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=LANGUAGE.split('-')[0] if LANGUAGE else None,  # Extract lang code
            )
        
        text = response.text.lower().strip()
        print(f"Transcribed: {text}")
        
        # Clean up
        os.unlink(wav_file)
        
        return text if text else ""
        
    except Exception as e:
        print(f"Transcription error: {e}")
        try:
            os.unlink(wav_file)
        except:
            pass
        return ""

if __name__ == "__main__":
    print("Testing Whisper speech-to-text")
    print("=" * 60)
    
    # Show available microphones
    print("\nAvailable microphones:")
    for name in get_microphone_names():
        print(f"  {name}")
    
    # Test recording and transcription
    print("\nPlease say something...")
    text = listen_whisper(duration=5)
    print(f"Result: {text if text else '(nothing recognized)'}")
