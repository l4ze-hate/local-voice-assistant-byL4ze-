import re
from config import WAKE_WORD


def _normalize(text):
    text = (text or "").lower().strip()
    # Keep letters/numbers/spaces only to reduce STT punctuation noise.
    text = re.sub(r"[^a-zа-я0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _wake_variants():
    base = _normalize(WAKE_WORD)
    variants = {
        base,
        "jarvis",
        "jarvix",
        "джарвис",
        "жарвис",
        "джервис",
        "джарвикс",
        "жарвикс",
    }
    return {item for item in variants if item}

def detect(text):
    normalized_text = _normalize(text)
    if not normalized_text:
        return False

    return any(variant in normalized_text for variant in _wake_variants())


def extract_command(text):
    normalized_text = _normalize(text)
    if not normalized_text:
        return ""

    for variant in sorted(_wake_variants(), key=len, reverse=True):
        if variant in normalized_text:
            command = normalized_text.replace(variant, "", 1).strip()
            return command
    return ""