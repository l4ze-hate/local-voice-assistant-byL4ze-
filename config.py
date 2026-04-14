from dotenv import load_dotenv
import os

# Load defaults from .env, then override from key.env if present.
load_dotenv()
load_dotenv("key.env", override=True)

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
WAKE_WORD = "JARVIS"
LANGUAGE = "ru-RU"
MICROPHONE_INDEX = os.getenv("MICROPHONE_INDEX")
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "edge")
TTS_VOICE = os.getenv("TTS_VOICE", "ru-RU-SvetlanaNeural")