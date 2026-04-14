#!/usr/bin/env python
"""
Test complete voice assistant cycle:
1. AI generates response
2. TTS speaks the response  
"""

print('TESTING AI VOICE RESPONSE')
print('=' * 60)

from assistant.ai_module import ask_ai
from assistant.text_to_speech import speak

# Test with Groq API
test_question = "Какой сейчас час?"

print(f'\nQuestion: {test_question}')
print('Asking AI...')

response = ask_ai(test_question)
print(f'AI Response: {response[:100]}...\n')

if response:
    print('Speaking response...')
    speak(response[:150])  # Speak first 150 chars
    print('\nDone!')
else:
    print('ERROR: No AI response')

print()
print('=' * 60)
