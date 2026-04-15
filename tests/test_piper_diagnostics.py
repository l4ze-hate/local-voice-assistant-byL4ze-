#!/usr/bin/env python
"""
Diagnostic: Test Piper TTS setup
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("PIPER TTS DIAGNOSTICS")
print("=" * 60)

try:
    from assistant.text_to_speech import _get_piper_path, _download_piper_voice
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

piper_exe = _get_piper_path()
print(f"\n1. Piper executable:")
print(f"   Path: {piper_exe}")
print(f"   Exists: {os.path.exists(piper_exe) if piper_exe else False}")

cache_dir = ".cache/piper_voices"
print(f"\n2. Voice cache directory: {cache_dir}")
print(f"   Exists: {os.path.exists(cache_dir)}")

if os.path.exists(cache_dir):
    files = os.listdir(cache_dir)
    print(f"   Files: {files if files else '(empty)'}")

print(f"\n3. Testing voice download...")
success = _download_piper_voice("ru_RU", cache_dir)
print(f"   Result: {'SUCCESS' if success else 'FAILED'}")

if os.path.exists(cache_dir):
    files = os.listdir(cache_dir)
    print(f"   Files after: {files}")

print()
print("=" * 60)
