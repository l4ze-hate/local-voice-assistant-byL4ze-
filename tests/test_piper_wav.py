#!/usr/bin/env python
"""
Test Piper WAV generation directly
"""
import subprocess
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("PIPER DIRECT WAV GENERATION TEST")
print("=" * 60)

# Find piper
from assistant.text_to_speech import _get_piper_path
piper_exe = _get_piper_path()
print(f"Piper: {piper_exe}")

if not piper_exe:
    print("ERROR: Piper not found")
    sys.exit(1)

# Create temp WAV file
with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
    temp_wav = f.name

text = "Привет, тестовый голос"
print(f"Text: {text}")
print(f"Output: {temp_wav}")

# Run piper command
print("\nRunning Piper...")
cmd = [
    piper_exe,
    "--output-file", temp_wav,
    "--voice", "ru_RU",
    "--download-dir", ".cache/piper_voices",
]

process = subprocess.run(
    cmd,
    input=text.encode("utf-8"),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    timeout=60,
)

print(f"Return code: {process.returncode}")
print(f"Stdout: {process.stdout.decode('utf-8', errors='ignore')[:200]}")
print(f"Stderr: {process.stderr.decode('utf-8', errors='ignore')[:200]}")

# Check WAV file
if os.path.exists(temp_wav):
    size = os.path.getsize(temp_wav)
    print(f"\nWAV file created: {size} bytes")
    
    if size > 0:
        print("✓ Piper generated audio successfully")
        
        # Try to play it
        print("\nAttempting playback with winsound...")
        try:
            import winsound
            winsound.PlaySound(temp_wav, winsound.SND_FILENAME | winsound.SND_SYNC)
            print("✓ Playback completed")
        except Exception as e:
            print(f"✗ Playback error: {e}")
    else:
        print("✗ WAV file is empty")
    
    # Clean up
    os.remove(temp_wav)
else:
    print(f"\n✗ WAV file not created at {temp_wav}")

print()
print("=" * 60)
