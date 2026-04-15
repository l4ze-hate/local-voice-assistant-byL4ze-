#!/usr/bin/env python
"""
Full diagnostic: Test voice assistant response with speak()
"""
import sys
import os
sys.path.insert(0, '.')

print("VOICE ASSISTANT DIAGNOSTICS")
print("=" * 70)

# Test 1: Configuration
print("\n1. CONFIGURATION")
from config import TTS_PROVIDER, TTS_VOICE, AI_PROVIDER, GROQ_MODEL
print(f"   TTS_PROVIDER: {TTS_PROVIDER}")
print(f"   TTS_VOICE: {TTS_VOICE}")
print(f"   AI_PROVIDER: {AI_PROVIDER}")

# Test 2: Piper executable
print("\n2. PIPER EXECUTABLE")
from assistant.text_to_speech import _get_piper_path
piper = _get_piper_path()
print(f"   Path: {piper}")
print(f"   Exists: {os.path.exists(piper) if piper else False}")

# Test 3: AI response
print("\n3. AI RESPONSE (Groq)")
from assistant.ai_module import ask_ai
try:
    response = ask_ai("Привет")
    print(f"   Response: {response[:80]}...")
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

# Test 4: Direct TTS
print("\n4. DIRECT TTS TEST")
from assistant.text_to_speech import speak
print("   Speaking test phrase...")
speak("Привет, это тест голоса")
print("   Playback should have occurred")

# Test 5: Combined AI + Voice
print("\n5. COMBINED TEST: AI answer read aloud")
question = "Кто ты?"
print(f"   Question: {question}")
answer = ask_ai(question)
print(f"   AI Answer: {answer[:100]}...")
print("   Speaking answer (first 100 chars)...")
speak(answer[:100])

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("\nIf you heard voice output:")
print("  ✓ System working correctly!")
print("\nIf you DID NOT hear voice:")
print("  1. Check Windows volume (System tray)")
print("  2. Check if speakers are connected/plugged in")
print("  3. Check app volume in Volume mixer (search 'Volume mixer')")
print("  4. Check if Piper generated WAV files in .cache/piper_voices")
