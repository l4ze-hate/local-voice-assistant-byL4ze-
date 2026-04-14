# JarviX Assistant

A Python-based voice assistant with speech recognition, AI integration, and GUI.

## Features
- Wake word activation ("JarviX")
- Voice commands
- **Multiple AI providers**: Groq (free, fast), Ollama (local), LM Studio, or OpenAI
- Speech-to-text and text-to-speech
- Desktop GUI with CustomTkinter
- Response caching

## Technologies
- Python
- SpeechRecognition
- pyttsx3
- OpenAI Python SDK (compatible with local servers and Groq)
- CustomTkinter
- Edge TTS
- Groq API

## Installation

```bash
pip install -r requirements.txt
```

## Environment setup

Edit `key.env` with your configuration:

```env
# Choose provider: "groq", "openai", or "local"
AI_PROVIDER=groq

# For Groq (FREE, no installation needed):
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=mixtral-8x7b-32768

# For OpenAI provider:
# OPEN_API_KEY=your-key-here
# OPENAI_MODEL=gpt-4o-mini

# For local provider (Ollama/LM Studio):
# LOCAL_AI_URL=http://localhost:11434
# LOCAL_AI_MODEL=llama2

# Audio
# MICROPHONE_INDEX=1
```

## Quick Start with Groq (RECOMMENDED - FREE & FASTEST)

### 1. Get Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up
3. Copy your API key

### 2. Update `key.env`
```env
AI_PROVIDER=groq
GROQ_API_KEY=<your-key-here>
```

### 3. Run
```bash
python main.py
```

✅ **No installation needed, instant replies!**

---

## Alternative: Local with Ollama

### 1. Install Ollama
Download from [ollama.ai](https://ollama.ai)

### 2. Pull a model
```bash
ollama pull llama2
```

### 3. Start Ollama (runs on http://localhost:11434)
```bash
ollama serve
```

### 4. Update `key.env`
```env
AI_PROVIDER=local
LOCAL_AI_URL=http://localhost:11434
LOCAL_AI_MODEL=llama2
```

### 5. Run the assistant
```bash
python main.py
```

---

## Alternative: LM Studio

1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Load a model and start the server (default: http://localhost:1234)
3. Update `key.env`:
```env
AI_PROVIDER=local
LOCAL_AI_URL=http://localhost:1234
LOCAL_AI_MODEL=<your-model-name>
```
4. Run: `python main.py`

---

## Configuration

- `.env` - default settings (committed to repo)
- `key.env` - your local overrides (gitignored for privacy)
