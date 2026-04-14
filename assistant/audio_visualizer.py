"""Audio level monitor and visualizer for the GUI."""
import threading
import time
import sounddevice as sd
import numpy as np


class AudioLevelMonitor:
    """Monitors microphone audio level in real-time."""

    def __init__(self, device_index=None):
        self.device_index = device_index
        self.current_level = 0.0
        self.is_active = False
        self._stream = None
        self._lock = threading.Lock()

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            pass
        with self._lock:
            rms = np.sqrt(np.mean(indata ** 2))
            self.current_level = min(rms / 0.1, 1.0)

    def start(self):
        """Start monitoring audio levels."""
        if self.is_active:
            return

        self.is_active = True
        try:
            self._stream = sd.InputStream(
                device=self.device_index,
                channels=1,
                samplerate=16000,
                callback=self._audio_callback,
                blocksize=512,
                dtype='float32'
            )
            self._stream.start()
        except Exception:
            self.is_active = False

    def stop(self):
        """Stop monitoring audio levels."""
        self.is_active = False
        if self._stream:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        with self._lock:
            self.current_level = 0.0

    def get_level(self):
        """Get current audio level (0.0 to 1.0)."""
        with self._lock:
            return self.current_level
