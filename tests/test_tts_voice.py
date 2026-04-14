#!/usr/bin/env python
"""
Test TTS directly
"""
print('TESTING TEXT-TO-SPEECH')
print('=' * 60)

from assistant.text_to_speech import speak
import time

# Test different phrases
test_phrases = [
    "Привет",
    "Я готов слушать команды",
    "Это тест голоса",
]

for i, phrase in enumerate(test_phrases, 1):
    print(f'\n{i}. Testing: "{phrase}"')
    print('   Speaking...')
    speak(phrase)
    print('   Done - did you hear it?')
    time.sleep(1)

print('\n' + '=' * 60)
print('If you heard nothing:')
print('1. Check Windows volume (is it at 100%?)')
print('2. Check if speakers are plugged in')
print('3. Unmute application in volume mixer')
