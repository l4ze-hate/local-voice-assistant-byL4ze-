import webbrowser
import datetime
from text_to_speech import speak

def execute(command):
    if "время" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"Сейчас {now}")
        
    elif "открой браузер" in command:
        webbrowser.open("https://www.google.com")
        speak("Открываю браузер")
        
    elif "Открой ютуб" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Открываю YouTube")
        
    elif "Конец работы" in command:
        speak("До встречи!")
        exit
    
    else:
        speak("Неизвестная команда")