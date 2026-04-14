import importlib
from config import LANGUAGE

try:
    sr = importlib.import_module("speech_recognition")
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Missing dependency 'SpeechRecognition'. Install it with: pip install SpeechRecognition"
    ) from exc

def listen():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio, language=LANGUAGE)
        return text.lower()
    except:
        return ""