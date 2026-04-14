#!/usr/bin/env python
"""
Alternative speech-to-text solutions comparison
"""

import os
import sounddevice
import numpy as np
import wave

print('Comparing speech-to-text solutions')
print('=' * 60)

# Solution 1: Google Speech-to-Text (current - doesn't work well)
print()
print('1. Google Speech-to-Text')
print('   - Pros: Built-in with SpeechRecognition, per-request')
print('   - Cons: Low-level signals get rejected')
print('   - Status: ❌ Not working reliably')

# Solution 2: OpenAI Whisper API
print()
print('2. OpenAI Whisper API')
print('   - Pros: Better accuracy, handles background noise')
print('   - Cons: Requires API key (free tier available)')
print('   - Cost: $0.02 per 1 min audio')
print('   - Setup: pip install openai')
print('   - Usage: client.audio.transcriptions.create()')

# Solution 3: Local Whisper (openai/whisper)
print()
print('3. Local Whisper (offline)')
print('   - Pros: Free, offline, no API key needed')
print('   - Cons: Slow (requires GPU or CPU time)')
print('   - Setup: pip install openai-whisper')
print('   - Usage: model.transcribe("audio.mp3")')

# Solution 4: Azure Speech-to-Text
print()
print('4. Azure Speech Services')
print('   - Pros: Good accuracy, reliable')
print('   - Cons: Requires Azure account + API key')
print('   - Cost: Free tier 5K requests/month')
print('   - Setup: pip install azure-cognitiveservices-speech')

# Solution 5: Groq Speech-to-Text  
print()
print('5. Groq Speech API (if available)')
print('   - Pros: Fast, already have API key')
print('   - Cons: May not be available/free')
print('   - Check docs: https://console.groq.com/docs')

print()
print('RECOMMENDATION:')
print('Use OpenAI Whisper API - good balance of:')
print('  • Accuracy (handles low-level signals)')
print('  • Cost (free tier covers typical use)')
print('  • Simplicity (one API key)')
print()
print('Or use local Whisper if you want offline capability')
