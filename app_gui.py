import customtkinter as ctk
from assistant.brain import run, request_stop
from assistant.speech_to_text import get_microphone_names, set_microphone_index, listen, set_vad_enabled, is_vad_enabled
from assistant.text_to_speech import set_tts_provider, get_tts_provider
from assistant.audio_visualizer import AudioLevelMonitor
from assistant.history_manager import CommandHistory
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Modern grey/black color palette
COLORS = {
    "bg_primary": "#1A1A1A",       # Dark background
    "bg_secondary": "#2A2A2A",     # Card background
    "bg_tertiary": "#3A3A3A",      # Hover/active
    "text_primary": "#F5F5F5",     # Primary text
    "text_secondary": "#B0B0B0",   # Secondary text
    "accent": "#5A5A5A",           # Accent color
    "accent_hover": "#6A6A6A",     # Accent hover
    "border": "#444444",           # Border color
    "success": "#4CAF50",          # Success/active
    "idle": "#888888",             # Idle status
    "warning": "#FF9800",          # Warning level
    "danger": "#F44336",           # High level
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JarviX Assistant")
        self.geometry("850x600")
        self.minsize(750, 550)

        self.configure(fg_color=COLORS["bg_primary"])

        self.is_running = False
        self.build_tag = "build-2026-04-14-v2"

        # Initialize new components
        self.audio_monitor = AudioLevelMonitor()
        self.history = CommandHistory()
        self.showing_history = True

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_card = ctk.CTkFrame(self, corner_radius=18, fg_color=COLORS["bg_secondary"])
        self.main_card.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        self.main_card.grid_columnconfigure(0, weight=1)
        self.main_card.grid_rowconfigure(2, weight=1)

        self.header = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=20, pady=(18, 10), sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self.header,
            text="🎙️ JarviX Assistant",
            font=("Segoe UI", 30, "bold"),
            anchor="w",
            text_color=COLORS["text_primary"],
        )
        self.label.grid(row=0, column=0, sticky="w")

        self.status = ctk.CTkLabel(
            self.header,
            text="● Status: Idle",
            font=("Segoe UI", 14),
            text_color=COLORS["idle"],
        )
        self.status.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.build_label = ctk.CTkLabel(
            self.header,
            text=f"Version: {self.build_tag}",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
            anchor="e",
        )
        self.build_label.grid(row=0, column=1, sticky="e")

        # Audio level indicator
        self.audio_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.audio_frame.grid(row=1, column=1, sticky="e", padx=(20, 0))

        self.audio_label = ctk.CTkLabel(
            self.audio_frame,
            text="Audio Level:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self.audio_label.grid(row=0, column=0, padx=(0, 5))

        self.audio_bar = ctk.CTkProgressBar(
            self.audio_frame,
            width=150,
            height=8,
            corner_radius=4,
            fg_color=COLORS["bg_tertiary"],
            progress_color=COLORS["success"],
        )
        self.audio_bar.grid(row=0, column=1)
        self.audio_bar.set(0)

        self.subtitle = ctk.CTkLabel(
            self.main_card,
            text="📝 Voice activity log",
            font=("Segoe UI", 15),
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        self.subtitle.grid(row=1, column=0, padx=20, pady=(2, 8), sticky="ew")

        # Mode toggle buttons
        self.mode_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.mode_frame.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="w")

        self.log_btn = ctk.CTkButton(
            self.mode_frame,
            text="📋 Log",
            width=80,
            height=28,
            command=self.show_log_mode,
            font=("Segoe UI", 12),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_primary"],
        )
        self.log_btn.grid(row=0, column=0, padx=(0, 5))

        self.history_btn = ctk.CTkButton(
            self.mode_frame,
            text="📚 History",
            width=80,
            height=28,
            command=self.show_history_mode,
            font=("Segoe UI", 12),
            fg_color=COLORS["bg_tertiary"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
        )
        self.history_btn.grid(row=0, column=1)

        self.textbox = ctk.CTkTextbox(
            self.main_card,
            corner_radius=12,
            font=("Consolas", 14),
            border_width=1,
            border_color=COLORS["border"],
            fg_color=COLORS["bg_primary"],
            text_color=COLORS["text_primary"],
        )
        self.textbox.grid(row=3, column=0, padx=20, pady=(0, 14), sticky="nsew")
        self.textbox.insert("end", "Assistant replies will appear here.\n")
        self.textbox.configure(state="disabled")

        # Search box for history
        self.search_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.search_frame.grid(row=3, column=0, padx=20, pady=(0, 14), sticky="ew")
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Search history...",
            height=32,
            font=("Segoe UI", 13),
            fg_color=COLORS["bg_primary"],
            border_color=COLORS["border"],
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.on_search_change())

        self.search_frame.grid_forget()

        self.mic_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.mic_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.mic_frame.grid_columnconfigure(1, weight=1)

        self.mic_label = ctk.CTkLabel(
            self.mic_frame,
            text="🎤 Microphone:",
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
        )
        self.mic_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.mic_options_map = {}
        self.mic_selector = ctk.CTkOptionMenu(
            self.mic_frame,
            values=["Default"],
            command=self.on_mic_selected,
            fg_color=COLORS["bg_tertiary"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
        )
        self.mic_selector.grid(row=0, column=1, sticky="ew")

        self.mic_refresh = ctk.CTkButton(
            self.mic_frame,
            text="🔄 Refresh",
            width=90,
            command=self.refresh_microphones,
            fg_color=COLORS["bg_tertiary"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
        )
        self.mic_refresh.grid(row=0, column=2, padx=(10, 0), sticky="e")

        # VAD toggle
        self.vad_var = ctk.BooleanVar(value=is_vad_enabled())
        self.vad_checkbox = ctk.CTkCheckBox(
            self.mic_frame,
            text="VAD",
            variable=self.vad_var,
            command=self.on_vad_toggle,
            font=("Segoe UI", 12),
            text_color=COLORS["text_primary"],
        )
        self.vad_checkbox.grid(row=0, column=3, padx=(10, 0), sticky="e")

        # TTS provider selector
        self.tts_label = ctk.CTkLabel(
            self.mic_frame,
            text="TTS:",
            font=("Segoe UI", 12),
            text_color=COLORS["text_secondary"],
        )
        self.tts_label.grid(row=0, column=4, padx=(10, 0), sticky="w")

        current_tts = get_tts_provider().lower()
        self.tts_var = ctk.StringVar(value="Edge" if current_tts == "edge" else "Piper")
        self.tts_selector = ctk.CTkOptionMenu(
            self.mic_frame,
            values=["Edge", "Piper"],
            command=self.on_tts_provider_changed,
            variable=self.tts_var,
            width=80,
            font=("Segoe UI", 12),
            fg_color=COLORS["bg_tertiary"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
        )
        self.tts_selector.grid(row=0, column=5, padx=(5, 0), sticky="w")

        self.controls = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.controls.grid(row=5, column=0, padx=20, pady=(0, 18), sticky="ew")
        self.controls.grid_columnconfigure((0, 1, 2), weight=1)

        self.start_button = ctk.CTkButton(
            self.controls,
            text="▶ Start JarviX",
            command=self.start,
            height=42,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_primary"],
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.stop_button = ctk.CTkButton(
            self.controls,
            text="⏛ Stop",
            command=self.stop,
            height=42,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            fg_color="#C0392B",
            hover_color="#E74C3C",
            text_color=COLORS["text_primary"],
        )
        self.stop_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.stop_button.grid_remove()  # Hide stop button initially

        self.clear_button = ctk.CTkButton(
            self.controls,
            text="🗑 Clear Log",
            command=self.clear_log,
            height=42,
            corner_radius=12,
            fg_color=COLORS["bg_tertiary"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            font=("Segoe UI", 14),
        )
        self.clear_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        self.test_button = ctk.CTkButton(
            self.controls,
            text="🎵 Mic Test",
            command=self.mic_test,
            height=42,
            corner_radius=12,
            fg_color=COLORS["bg_tertiary"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text_primary"],
            font=("Segoe UI", 14),
        )
        self.test_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))
        self.refresh_microphones()

        # Start audio level monitoring update loop
        self.update_audio_level()

    def _append_log(self, text):
        if not text.startswith("AI:"):
            return

        response_text = text.replace("AI: ", "", 1)

        # Add to history
        if hasattr(self, '_last_command'):
            self.history.add_entry(self._last_command, response_text)
            del self._last_command

        # Update textbox
        self.textbox.configure(state="normal")
        self.textbox.insert("end", response_text + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def log(self, text):
        # run() works in a background thread; UI updates must happen on main thread
        self.after(0, self._append_log, text)

    def log_command(self, command):
        """Log a user command for history tracking."""
        self._last_command = command
        self.after(0, self._append_command_to_log, command)

    def _append_command_to_log(self, command):
        """Append command to the log display."""
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f">>> {command}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear_log(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "Log cleared.\n")
        self.textbox.configure(state="disabled")

    def show_log_mode(self):
        """Show regular log mode."""
        self.showing_history = True
        self.search_frame.grid_forget()
        self.textbox.grid(row=3, column=0, padx=20, pady=(0, 14), sticky="nsew")
        self.log_btn.configure(fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"])
        self.history_btn.configure(fg_color=COLORS["bg_tertiary"], hover_color=COLORS["accent"])

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("end", "Assistant replies will appear here.\n")
        self.textbox.configure(state="disabled")

    def show_history_mode(self):
        """Show history mode with search."""
        self.showing_history = False
        self.textbox.grid_forget()
        self.search_frame.grid(row=3, column=0, padx=20, pady=(0, 14), sticky="ew")
        self.log_btn.configure(fg_color=COLORS["bg_tertiary"], hover_color=COLORS["accent"])
        self.history_btn.configure(fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"])

        self.search_entry.delete(0, "end")
        self._display_history()

    def _display_history(self, filtered=None):
        """Display history in textbox."""
        entries = filtered if filtered is not None else self.history.get_all()

        self.textbox.grid(row=3, column=0, padx=20, pady=(0, 14), sticky="nsew")
        self.search_frame.grid(row=4, column=0, padx=20, pady=(0, 14), sticky="ew")

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        if not entries:
            self.textbox.insert("end", "No history entries yet.\n")
        else:
            for entry in reversed(entries):
                self.textbox.insert("end", f"[{entry['timestamp']}] {entry['command']}\n")
                self.textbox.insert("end", f"  → {entry['response']}\n\n")

        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def on_search_change(self):
        """Handle search input change."""
        query = self.search_entry.get()
        if query:
            filtered = self.history.search(query)
            self._display_history(filtered)
        else:
            self._display_history()

    def update_audio_level(self):
        """Update the audio level indicator."""
        if self.audio_monitor.is_active:
            level = self.audio_monitor.get_level()
            self.audio_bar.set(level)

            # Change color based on level
            if level > 0.5:
                self.audio_bar.configure(progress_color=COLORS["danger"])
            elif level > 0.2:
                self.audio_bar.configure(progress_color=COLORS["warning"])
            else:
                self.audio_bar.configure(progress_color=COLORS["success"])

        # Schedule next update (50ms = 20 FPS)
        self.after(50, self.update_audio_level)

    def refresh_microphones(self):
        names = get_microphone_names()
        values = ["Default"]
        self.mic_options_map = {"Default": None}

        for index, name in enumerate(names):
            label = f"[{index}] {name}"
            values.append(label)
            self.mic_options_map[label] = index

        self.mic_selector.configure(values=values)
        self.mic_selector.set("Default")
        set_microphone_index(None)

    def on_mic_selected(self, value):
        index = self.mic_options_map.get(value)
        set_microphone_index(index)

    def on_vad_toggle(self):
        """Handle VAD toggle."""
        set_vad_enabled(self.vad_var.get())

    def on_tts_provider_changed(self, value):
        """Handle TTS provider change."""
        provider = value.lower()
        set_tts_provider(provider)
        print(f"TTS provider changed to: {value}")

    def _run_mic_test(self):
        heard = listen()
        if heard:
            self.log_command(heard)
            self.log(f"AI: Mic test: {heard}")
        else:
            self.log("AI: Mic test: [no speech recognized]")
        self.after(0, lambda: self.test_button.configure(state="normal", text="🎵 Mic Test"))

    def mic_test(self):
        if self.is_running:
            return
        self.test_button.configure(state="disabled", text="Testing...")
        threading.Thread(target=self._run_mic_test, daemon=True).start()

    def on_session_end(self):
        """Handle assistant session end (from brain.py)."""
        self.is_running = False
        self.start_button.grid()  # Show start button
        self.stop_button.grid_remove()  # Hide stop button
        self.status.configure(text="● Status: Idle", text_color=COLORS["idle"])

        # Stop audio monitoring
        self.audio_monitor.stop()
        self.audio_bar.set(0)

    def _run_assistant(self):
        try:
            run(self.log, self.log_command)
        except Exception:
            self.after(0, self.on_session_end)
            self.log("AI: Произошла ошибка в ассистенте.")
        finally:
            self.after(0, self.on_session_end)

    def start(self):
        if self.is_running:
            return

        self.is_running = True
        self.start_button.grid_remove()  # Hide start button
        self.stop_button.grid()  # Show stop button
        self.status.configure(text="● Status: Listening", text_color=COLORS["success"])

        # Start audio monitoring
        self.audio_monitor.start()

        threading.Thread(target=self._run_assistant, daemon=True).start()

    def stop(self):
        """Stop the assistant."""
        if not self.is_running:
            return

        self.is_running = False
        self.start_button.grid_remove()  # Keep both hidden temporarily
        self.stop_button.grid_remove()
        self.status.configure(text="● Status: Stopping...", text_color=COLORS["warning"])

        # Request brain to stop
        request_stop()

        # Stop audio monitoring immediately
        self.audio_monitor.stop()
        self.audio_bar.set(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
