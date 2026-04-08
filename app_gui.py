import customtkinter as ctk
from assistant.brain import run
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("JarviX Assistant")
        self.geometry("500x500")
        
        self.label = ctk.CTkLabel(self, text="JarviX", font=("Arial", 24))
        self.label.pack(pady=20)
        
        self.textbox = ctk.Textbox(self, width=400, height=200)
        self.textbox.pack(pady=10)
        
        self.button = ctk.CTkButton(self, text="Start JarviX", command=self.start)
        self.button.pack(pady=20)
        
    def log(self, text):
        self.textbox.insert("end", text + "\n")
        self.textbox.see("end")
        
    def start(self):
        threading.Thread(target=run, args=(self.log,), daemon=True).start()
            
if __name__ == "__main__":
    app = App()
    app.mainloop()