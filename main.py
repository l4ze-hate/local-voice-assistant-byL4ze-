from assistant.speech_to_text import listen
from assistant.commands import execute
from assistant.text_to_speech import speak

speak("Ассистент готов к работе")
    
while True:
    command = listen()
    if command:
        execute(command)