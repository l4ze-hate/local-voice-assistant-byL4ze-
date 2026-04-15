"""Simple energy-based Voice Activity Detection (VAD)."""
import numpy as np


class SimpleVADDetector:
    """Energy-based VAD detector using RMS level."""

    def __init__(self, sample_rate=16000):
        """
        Initialize simple VAD detector.

        Args:
            sample_rate: Audio sample rate (default 16000 Hz)
        """
        self.sample_rate = sample_rate
        self.is_speaking = False
        self.silence_frames = 0
        self.speech_frames = 0

        # Thresholds (tuned for 16-bit audio)
        self.speech_threshold = 0.02  # RMS level to consider speech
        self.silence_threshold = 0.01  # RMS level to consider silence

        # Frame counts for stability
        self.min_speech_frames = 3    # ~60ms of speech before starting
        self.max_silence_frames = 20  # ~400ms of silence before stopping

    def calculate_rms(self, audio_frame):
        """Calculate RMS level of audio frame."""
        if isinstance(audio_frame, np.ndarray):
            audio_float = audio_frame.astype(np.float32)
        else:
            audio_float = np.frombuffer(audio_frame, dtype=np.int16).astype(np.float32)

        # Normalize to [-1, 1]
        audio_float = audio_float / 32768.0
        rms = np.sqrt(np.mean(audio_float ** 2))
        return rms

    def process_frame(self, audio_frame):
        """
        Process an audio frame and detect speech boundaries.

        Args:
            audio_frame: Audio frame data (numpy array or bytes)

        Returns:
            str: 'start' (speech began), 'end' (speech ended), 'speaking', or 'silent'
        """
        rms = self.calculate_rms(audio_frame)

        if rms > self.speech_threshold:
            self.speech_frames += 1
            self.silence_frames = 0

            if not self.is_speaking and self.speech_frames >= self.min_speech_frames:
                self.is_speaking = True
                return 'start'
            elif self.is_speaking:
                return 'speaking'
            else:
                return 'silent'
        elif rms < self.silence_threshold:
            self.speech_frames = 0

            if self.is_speaking:
                self.silence_frames += 1
                if self.silence_frames >= self.max_silence_frames:
                    self.is_speaking = False
                    return 'end'
                return 'speaking'
            else:
                return 'silent'
        else:
            # In between thresholds, maintain state
            if self.is_speaking:
                return 'speaking'
            else:
                return 'silent'

    def reset(self):
        """Reset detector state."""
        self.is_speaking = False
        self.silence_frames = 0
        self.speech_frames = 0
