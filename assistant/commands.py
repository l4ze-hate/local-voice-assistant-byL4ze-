import webbrowser
import datetime

def execute(command):
    command = command.lower()

    if "время" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"Сейчас {now}"

    if "открой браузер" in command or "open browser" in command:
        webbrowser.open("https://www.google.com")
        return "Открываю браузер"

    if "открой ютуб" in command or "открой youtube" in command or "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Открываю YouTube"

    if "конец работы" in command or "stop" in command or "exit" in command:
        return "exit"

    return None
