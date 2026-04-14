from assistant.speech_to_text import listen
from assistant.text_to_speech import speak
from assistant.ai_module import ask_ai
from assistant.commands import execute
from assistant.wake_word import detect

def run(callback=None):
    speak("Ассистент готов к работе")
    
    while True:
        text = listen()
        
        if not text:
            continue
        
        if callback:
            callback(f"You: {text}")
            
        if detect(text):
            speak("Слушаю вас")
            
            command = listen()
            
            if callback:
                callback(f"Command: {command}")
                
            result = execute(command)
            
            if result == "exit":
                speak("Выключаюсь")
                break
            
            if result:
                speak(result)
                if callback:
                    callback(f"AI: {result}")
                    
            else:
                answer = ask_ai(command)
                speak(answer)
                if callback:
                    callback(f"AI: {answer}")
                    
    speak("До встречи!")
    if callback:
        callback("Session ended")
        
    return True
    
if __name__ == "__main__":
    run()