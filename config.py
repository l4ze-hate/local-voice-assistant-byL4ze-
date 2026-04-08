from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные из .env

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
WAKE_WORD = "JARVIS"
LANGUAGE = "ru-RU"