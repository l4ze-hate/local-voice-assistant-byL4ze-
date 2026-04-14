import importlib


def _create_engine():
    try:
        pyttsx3 = importlib.import_module("pyttsx3")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: pyttsx3. Install with `pip install -r requirements.txt`."
        ) from exc
    return pyttsx3.init()
    

engine = _create_engine()


def speak(text):
    print("Ассистент: ", text)
    engine.say(text)
    engine.runAndWait()