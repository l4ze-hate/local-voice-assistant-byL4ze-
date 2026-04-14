import importlib
from config import LANGUAGE, MICROPHONE_INDEX

sr = None
_dependency_warning_shown = False
_microphone_warning_shown = False
_recognition_warning_shown = False
_microphone_list_shown = False
_selected_microphone_shown = False
_selected_microphone_index = None
_input_device_indices = []
_vad_enabled = True


def _get_sr():
    global sr, _dependency_warning_shown
    if sr is not None:
        return sr

    try:
        sr = importlib.import_module("speech_recognition")
    except ModuleNotFoundError:
        if not _dependency_warning_shown:
            print("Missing dependency: SpeechRecognition. Run `pip install -r requirements.txt`.")
            _dependency_warning_shown = True
        return None
    return sr


def _get_sounddevice():
    try:
        return importlib.import_module("sounddevice")
    except ModuleNotFoundError:
        return None


def _get_numpy():
    try:
        return importlib.import_module("numpy")
    except ModuleNotFoundError:
        return None


def get_microphone_names():
    global _input_device_indices

    sounddevice = _get_sounddevice()
    if sounddevice is not None:
        try:
            devices = sounddevice.query_devices()
            names = []
            indices = []
            for index, device in enumerate(devices):
                if device.get("max_input_channels", 0) > 0:
                    names.append(device.get("name", f"Input {index}"))
                    indices.append(index)
            _input_device_indices = indices
            return names
        except Exception:
            pass

    speech_recognition = _get_sr()
    if speech_recognition is None:
        _input_device_indices = []
        return []

    try:
        names = speech_recognition.Microphone.list_microphone_names()
        _input_device_indices = list(range(len(names)))
        return names
    except Exception:
        _input_device_indices = []
        return []


def set_microphone_index(index):
    global _selected_microphone_index, _selected_microphone_shown
    _selected_microphone_index = index
    _selected_microphone_shown = False


def get_selected_microphone_index():
    return _selected_microphone_index


def set_vad_enabled(enabled):
    """Enable or disable VAD."""
    global _vad_enabled
    _vad_enabled = enabled


def is_vad_enabled():
    """Check if VAD is enabled."""
    return _vad_enabled


def _resolve_device_index():
    if _selected_microphone_index is not None:
        if 0 <= _selected_microphone_index < len(_input_device_indices):
            return _input_device_indices[_selected_microphone_index]
        return None

    if MICROPHONE_INDEX:
        try:
            return int(MICROPHONE_INDEX)
        except ValueError:
            print(f"Invalid MICROPHONE_INDEX='{MICROPHONE_INDEX}'. Using default microphone.")
    return None


def _find_best_microphone():
    """Auto-detect the best working microphone by testing signal strength.
    
    Returns:
        Best device index or None to use system default
    """
    sounddevice = _get_sounddevice()
    numpy = _get_numpy()
    if sounddevice is None or numpy is None:
        return None
    
    # Candidate microphones to try (common real microphones, not virtual ones)
    candidates = []
    try:
        devices = sounddevice.query_devices()
        for i, device in enumerate(devices):
            name = device.get('name', '').lower()
            # Skip virtual devices (SteelSeries, Sonar, etc.)
            if device.get('max_input_channels', 0) > 0:
                if any(x in name for x in ['virtual', 'sonar', 'stream', 'mixer']):
                    continue
                # Prefer USBdevices and real microphones
                if any(x in name for x in ['microphone', 'mic', 'fifine', 'realtek', 'input']):
                    candidates.append(i)
    except:
        return None
    
    if not candidates:
        return None
    
    # Test each candidate
    best_device = None
    best_level = 0
    sample_rate = 16000
    test_duration = 1  # 1 second test
    
    for device_id in candidates[:5]:  # Test max 5 devices to not waste time
        try:
            audio = sounddevice.rec(
                int(test_duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype='int16',
                device=device_id,
                timeout=2
            )
            sounddevice.wait(timeout=2)
            
            # Measure signal strength
            level = max(abs(audio.min()), abs(audio.max()))
            if level > best_level:
                best_level = level
                best_device = device_id
        except:
            pass
    
    return best_device if best_level > 100 else None


def _record_with_sounddevice(speech_recognition, device_index, duration=6, sample_rate=16000):
    sounddevice = _get_sounddevice()
    numpy = _get_numpy()
    if sounddevice is None or numpy is None:
        return None

    frames = int(duration * sample_rate)
    
    # Record audio
    audio = sounddevice.rec(
        frames,
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        device=device_index,
    )
    sounddevice.wait()
    
    # Convert to numpy array
    audio = numpy.asarray(audio)
    
    # Amplify weak signals (common with some USB microphones)
    max_signal = max(abs(audio.min()), abs(audio.max()))
    if max_signal > 0 and max_signal < 5000:  # Weak signal threshold
        # Amplify to bring into better range for STT
        scale_factor = min(15000 / max_signal, 4.0)  # Cap amplification
        audio = (audio.astype(numpy.float32) * scale_factor).astype(numpy.int16)
    
    audio_bytes = audio.tobytes()
    return speech_recognition.AudioData(audio_bytes, sample_rate, 2)


def _listen_with_vad(speech_recognition, recognizer, device_index):
    """
    Listen with VAD for faster speech detection.
    
    Returns AudioData when speech is detected and completed.
    """
    sounddevice = _get_sounddevice()
    numpy = _get_numpy()
    
    if sounddevice is None or numpy is None:
        return None
    
    try:
        from assistant.vad import SimpleVADDetector
    except ImportError:
        return None
    
    vad = SimpleVADDetector(sample_rate=16000)
    sample_rate = 16000
    frame_duration = 0.020  # 20ms frames
    frame_size = int(sample_rate * frame_duration)  # 320 samples
    
    max_speech_duration = 8  # seconds
    max_frames = int(max_speech_duration / frame_duration)  # 400 frames
    
    audio_buffer = []
    frame_count = 0
    speech_started = False
    
    try:
        stream = sounddevice.InputStream(
            device=device_index,
            channels=1,
            samplerate=sample_rate,
            dtype='int16',
            blocksize=frame_size,
        )
        stream.start()
        
        while frame_count < max_frames:
            audio_frame, _ = stream.read(frame_size)
            
            vad_state = vad.process_frame(audio_frame)
            
            if vad_state == 'start':
                speech_started = True
                audio_buffer.append(audio_frame)
                frame_count += 1
            
            elif vad_state == 'speaking':
                if speech_started:
                    audio_buffer.append(audio_frame)
                    frame_count += 1
            
            elif vad_state == 'end':
                # Speech ended, return collected audio
                if speech_started and len(audio_buffer) > 5:
                    all_audio = numpy.concatenate(audio_buffer)
                    audio_bytes = all_audio.tobytes()
                    stream.stop()
                    stream.close()
                    return speech_recognition.AudioData(audio_bytes, sample_rate, 2)
                else:
                    # Too short, ignore
                    vad.reset()
                    audio_buffer = []
                    speech_started = False
            
            elif not speech_started:
                frame_count += 1
        
        # Timeout - return what we have if speech was detected
        if speech_started and len(audio_buffer) > 5:
            all_audio = numpy.concatenate(audio_buffer)
            audio_bytes = all_audio.tobytes()
            stream.stop()
            stream.close()
            return speech_recognition.AudioData(audio_bytes, sample_rate, 2)
        
        stream.stop()
        stream.close()
        return None
        
    except Exception:
        try:
            stream.stop()
            stream.close()
        except Exception:
            pass
        return None


def listen():
    global _microphone_warning_shown, _recognition_warning_shown, _microphone_list_shown, _selected_microphone_shown, _selected_microphone_index

    speech_recognition = _get_sr()
    if speech_recognition is None:
        return ""

    recognizer = speech_recognition.Recognizer()
    device_index = _resolve_device_index()
    
    # If no explicit microphone selected, try to find the best one
    if device_index is None:
        device_index = _find_best_microphone()

    try:
        if not _microphone_list_shown:
            names = get_microphone_names()
            print("Available microphones:")
            for index, name in enumerate(names):
                print(f"  [{index}] {name}")
            _microphone_list_shown = True

        if device_index is not None and not _selected_microphone_shown:
            print(f"Using microphone index: {device_index}")
            _selected_microphone_shown = True

        # Prefer sounddevice + numpy for more reliable microphone access
        sounddevice = _get_sounddevice()
        numpy = _get_numpy()
        
        if sounddevice is not None and numpy is not None:
            audio = _record_with_sounddevice(speech_recognition, device_index, duration=6, sample_rate=16000)
            if audio is None:
                return ""
        else:
            # Fallback to SpeechRecognition (requires PyAudio)
            with speech_recognition.Microphone(device_index=device_index) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
    except Exception as exc:
        # Keep app running even when microphone backend is unavailable.
        if not _microphone_warning_shown:
            print(f"Microphone error: {exc}")
            print(
                "Tip: install sounddevice + numpy, or python 3.12 with PyAudio."
            )
            _microphone_warning_shown = True
        return ""

    try:
        text = recognizer.recognize_google(audio, language=LANGUAGE)
        return text.lower()
    except speech_recognition.UnknownValueError:
        if not _recognition_warning_shown:
            print("Speech detected but could not recognize words clearly.")
            _recognition_warning_shown = True
        return ""
    except speech_recognition.RequestError as exc:
        print(f"Speech recognition service error: {exc}")
        return ""
    except Exception as exc:
        print(f"Unexpected speech recognition error: {exc}")
        return ""