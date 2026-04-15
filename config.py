from dotenv import load_dotenv
import os

# Load defaults from .env, then override from key.env if present.
load_dotenv()
load_dotenv("key.env", override=True)

# AI Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # "groq", "openai" или "local"
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

# Local AI Server Configuration (для Ollama, LM Studio и др.)
LOCAL_AI_URL = os.getenv("LOCAL_AI_URL", "http://localhost:11434")
LOCAL_AI_MODEL = os.getenv("LOCAL_AI_MODEL", "llama2")

# Voice Assistant Configuration
WAKE_WORD = "JARVIS"
LANGUAGE = "ru-RU"
MICROPHONE_INDEX = os.getenv("MICROPHONE_INDEX")
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "piper")  # Default: piper (offline)
TTS_VOICE = os.getenv("TTS_VOICE", "ru_RU")  # Piper voice name
