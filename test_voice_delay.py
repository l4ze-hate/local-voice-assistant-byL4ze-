#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test voice system with focus on microphone delay issue
This demonstrates that microphone needs to wait after speaker output
"""
import time
from assistant.text_to_speech import speak
from assistant.speech_to_text import listen

print("=" * 70)
print("VOICE DELAY TEST - Testing microphone after speaker")
print("=" * 70)

print("\n[TEST 1] TTS only - listen to voice")
print("-" * 70)
speak("Привет, это тест голосовой системы")
print("Did you hear the voice message above?")

print("\n[TEST 2] Without delay (OLD - PROBLEM)")
print("-" * 70)
print("This will try to listen immediately after speaking")
print("Microphone may pick up speaker output...")
speak("Сейчас я начну слушать мгновенно")
print("Listening without delay...")
# text = listen()  # Commented to avoid actual listening in this test
print("(Skipped listening to avoid speaker echo)")

print("\n[TEST 3] With delay (NEW - SOLUTION)")
print("-" * 70)
print("This waits 0.5 seconds after speaking before listening")
speak("Теперь я жду пол-секунды перед прослушиванием")
print("Waiting 0.5 seconds...")
time.sleep(0.5)
print("Now listening (microphone should be clear)...")
# text = listen()  # Commented out
print("(Ready to listen)")

print("\n[TEST 4] Full conversation test")
print("-" * 70)
print("Instructions:")
print("1. System will ask you to speak")
print("2. Say: 'JARVIS, какое сейчас время?'")
print("3. System should recognize 'jarvis' keyword")
print("4. System should respond with time")
print("\nStarting in 3 seconds...")
print("-" * 70)

time.sleep(3)

speak("Ассистент готов. Скажите JARVIS и ваш вопрос")
time.sleep(0.5)  # Critical delay before listening!

print("Listening for voice command...")
try:
    text = listen()
    if text:
        print(f"Recognized: {text}")
        
        from assistant.wake_word import detect, extract_command
        if detect(text):
            print("[OK] Wake word JARVIS detected!")
            command = extract_command(text)
            print(f"Command: {command}")
            
            if command:
                speak(f"Выполняю: {command}")
                # Could execute command or ask AI here
            else:
                speak("Я не понял команду")
        else:
            print("[INFO] Wake word not detected in: " + text)
            speak("Повторите, начните с JARVIS")
    else:
        print("No speech detected")
        speak("Я вас не услышал")
except Exception as e:
    print(f"Error: {e}")
    speak("Произошла ошибка при распознавании речи")

print("\n" + "=" * 70)
print("[SUMMARY]")
print("The key fix: Add time.sleep(0.5) after every speak() before listen()")
print("This prevents microphone from capturing its own speaker output")
print("=" * 70)
