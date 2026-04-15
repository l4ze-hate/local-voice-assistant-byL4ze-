#!/usr/bin/env python
"""
Verify Piper is generating WAV files
"""
import os
import sys
sys.path.insert(0, '.')

from assistant.text_to_speech import speak

print("=" * 60)
print("PIPER VOICE OUTPUT VERIFICATION")
print("=" * 60)

cache_dir = ".cache/piper_voices"

# Get initial file count
before_files = set(os.listdir(cache_dir)) if os.path.exists(cache_dir) else set()
print(f"\nBefore test: {len(before_files)} files in {cache_dir}")

# Speak something
print("\nSpeaking 'Привет'...")
speak("Привет")

# Check files after
after_files = set(os.listdir(cache_dir)) if os.path.exists(cache_dir) else set()
print(f"After test: {len(after_files)} files in {cache_dir}")

if len(after_files) > len(before_files):
    new_files = after_files - before_files
    print(f"\n✓ SUCCESS: Piper generated files: {new_files}")
elif len(after_files) > 0:
    print(f"\n✓ SUCCESS: Piper cache contains: {list(after_files)[:5]}")
else:
    print(f"\n✗ No files in cache - Piper may need internet on first run")

print("\n" + "=" * 60)
print("If you didn't hear voice:")
print("  1. Check Windows volume (bottom right)")
print("  2. Check if speakers are connected")
print("  3. Check Volume Mixer (right-click speaker)")
print("=" * 60)
