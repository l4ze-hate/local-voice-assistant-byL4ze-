# JarviX Assistant

A Python-based voice assistant with speech recognition, AI integration, and GUI.

## Features
- Wake word activation ("JarviX")
- Voice commands
- AI responses (OpenAI)
- Weather API integration
- Desktop GUI

## Technologies
- Python
- SpeechRecognition
- pyttsx3
- OpenAI API
- CustomTkinter

## Installation

```bash
pip install -r requirements.txt
```

## Environment setup

1. Copy `.env.example` to `.env`.
2. Put your real `OPEN_API_KEY` into `.env` or `key.env`.
3. Use `key.env` for private machine-specific overrides.

`.env` and `key.env` are ignored by Git. `.env.example` is safe to commit.
