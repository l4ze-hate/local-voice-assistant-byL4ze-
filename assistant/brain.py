from assistant.speech_to_text import listen
from assistant.text_to_speech import speak
from assistant.ai_module import ask_ai
from assistant.commands import execute
from assistant.wake_word import detect, extract_command
import threading
import logging

# Setup logging
logger = logging.getLogger('Brain')

_stop_event = threading.Event()

def request_stop():
    """Request the assistant to stop."""
    _stop_event.set()

def reset_stop():
    """Reset the stop event for a new session."""
    _stop_event.clear()

def is_stopped():
    """Check if stop was requested."""
    return _stop_event.is_set()

def run(callback=None, command_callback=None):
    reset_stop()
    logger.info("Assistant started")
    
    def emit(text):
        if callback:
            callback(f"AI: {text}")

    speak("Ассистент готов к работе")
    emit("Ассистент готов к работе")

    try:
        while True:
            # Check for stop request at the start of each loop
            if is_stopped():
                logger.info("Stop requested")
                break
                
            logger.info("Listening...")
            text = listen()
            if not text:
                continue

            logger.info(f"Recognized: {text}")
            speak(f"Распознал: {text}")
            emit(f"Распознал: {text}")

            if not detect(text):
                continue

            logger.info("Wake word detected")
            speak("Слушаю команду")

            # Support one-shot phrase: "jarvis open browser".
            command = extract_command(text)
            if not command:
                logger.info("No command in phrase, asking for clarification")
                speak("Пожалуйста, дайте команду")
                command = listen()

            if not command:
                logger.info("No command received")
                continue

            logger.info(f"Command: {command}")
            speak(f"Выполняю: {command}")
            
            # Send command to UI for logging
            if command_callback:
                command_callback(command)

            logger.info(f"Executing command: {command}")
            result = execute(command)

            if result == "exit":
                logger.info("Exit command received")
                speak("До встречи!")
                break

            if result:
                logger.info(f"Command executed: {result}")
                speak(result)
                emit(result)
            else:
                logger.info(f"Command not recognized, using AI: {command}")
                speak("Ищу ответ в базе знаний")
                answer = ask_ai(command)
                logger.info(f"AI response received ({len(answer)} chars)")
                speak(answer)
                emit(answer)
    finally:
        # Always clean up when exiting
        reset_stop()
        logger.info("Assistant stopped")

    speak("До встречи!")
    emit("До встречи!")
    
    return True

if __name__ == "__main__":
    run()