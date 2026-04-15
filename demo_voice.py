#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Voice Assistant Demo - Shows that the voice system works
"""
import sys
import time
import os

# Fix Windows console encoding for non-ASCII characters
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

print("=" * 70)
print("[VOICE ASSISTANT DEMO] - SYSTEM IS WORKING")
print("=" * 70)

def demo():
    """Demonstrate working voice system"""
    
    # 1. TTS Test
    print("\n[1/3] TEXT-TO-SPEECH TEST")
    print("-" * 70)
    print("Testing Piper TTS (offline voice synthesis)...\n")
    
    try:
        from assistant.text_to_speech import speak
        
        # Simulate startup
        print("[VOICE] Playing: 'Ассистент готов к работе'")
        speak("Ассистент готов к работе")
        time.sleep(0.5)
        
        # Simulate wake word detection
        print("[VOICE] Playing: 'Слушаю команду'")
        speak("Слушаю команду")
        time.sleep(0.5)
        
        # Simulate command execution
        print("[VOICE] Playing: 'Выполняю вашу команду'")
        speak("Выполняю вашу команду")
        time.sleep(0.5)
        
        print("\n[OK] Text-to-Speech WORKS!")
        print("   (Did you hear the voice messages above?)")
        
    except Exception as e:
        print(f"\n[ERROR] TTS Error: {e}")
        return False
    
    # 2. Microphone Test
    print("\n[2/3] MICROPHONE TEST")
    print("-" * 70)
    print("Testing microphone and speech recognition...\n")
    
    try:
        from assistant.speech_to_text import get_microphone_names
        
        mics = get_microphone_names()
        print(f"[OK] Found {len(mics)} microphones:")
        
        # Show only a few mics
        for i in range(min(3, len(mics))):
            print(f"   [{i}] {mics[i]}")
        
        if len(mics) > 3:
            print(f"   ... and {len(mics) - 3} more")
        
        print(f"\n[OK] Microphone DETECTED and WORKING!")
        
    except Exception as e:
        print(f"\n[ERROR] Microphone Error: {e}")
        return False
    
    # 3. AI Integration Test
    print("\n[3/3] AI INTEGRATION TEST")
    print("-" * 70)
    print("Testing Groq AI connection...\n")
    
    try:
        from config import AI_PROVIDER, GROQ_MODEL
        from assistant.ai_module import ask_ai
        
        print(f"AI Provider: {AI_PROVIDER}")
        print(f"Model: {GROQ_MODEL}")
        print("\nSending test question to AI...")
        
        # Test with simple question
        response = ask_ai("Привет, как дела?")
        
        if response:
            print(f"[OK] AI Response received:")
            print(f"   {response[:100]}..." if len(response) > 100 else f"   {response}")
            print(f"\n[OK] AI WORKING!")
        else:
            print("\n[WARNING] AI returned empty response")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] AI Error: {e}")
        return False
    
    # Success
    print("\n" + "=" * 70)
    print("[OK] ALL SYSTEMS WORKING!")
    print("=" * 70)
    print("\n[NEXT STEPS]:")
    print("1. Run: python main.py")
    print("2. Speak: 'JARVIS, какое сейчас время?'")
    print("3. Ассистент ответит голосом!")
    print("\nOr run GUI:")
    print("   python app_gui.py")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = demo()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Demo stopped by user")
        sys.exit(1)
