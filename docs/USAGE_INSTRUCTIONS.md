# 🎯 Использование Jarvis Voice Assistant

## 📦 Вариант 1: Готовый .exe файл (рекомендуется)

### Что нужно:
1. **JarvisGUI.exe** или **JarvisCLI.exe** (из папки `dist/` или релиза)
2. **Файл .env** с API ключом

### Пошаговая установка:

#### Шаг 1: Создание папки для ассистента
Создайте папку, например:
```
C:\Program Files\Jarvis\
```

#### Шаг 2: Копирование .exe файла
Скопируйте туда один из файлов:
- **JarvisGUI.exe** — для графического интерфейса (рекомендуется)
- **JarvisCLI.exe** — для консольного режима

#### Шаг 3: Создание файла конфигурации
Создайте файл `.env` в той же папке:

```env
# ========== Конфигурация Jarvis Voice Assistant ==========

# AI провайдер (groq, openai или local)
AI_PROVIDER=groq

# Groq API ключ (получите бесплатно на https://console.groq.com/keys)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Модель AI (по умолчанию)
GROQ_MODEL=llama-3.3-70b-versatile

# Синтез речи (edge или piper)
TTS_PROVIDER=edge

# Голос для Edge TTS (русский)
TTS_VOICE=ru-RU-SvetlanaNeural

# Индекс микрофона (оставьте пустым для авто-выбора)
MICROPHONE_INDEX=

# Локальный AI сервер (если используете Ollama/LM Studio)
# LOCAL_AI_URL=http://localhost:11434
# LOCAL_AI_MODEL=llama2
```

**ВАЖНО:** Замените `gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` на ваш реальный API ключ!

#### Шаг 4: Получение API ключа
1. Перейдите на https://console.groq.com/keys
2. Войдите в аккаунт (или создайте бесплатный)
3. Нажмите "Create API Key"
4. Скопируйте ключ (начинается с `gsk_`)
5. Вставьте в файл `.env`

#### Шаг 5: Запуск!
Дважды кликните по `.exe` файлу!

---

## 🎤 Как использовать

### JarvisGUI (графическая версия)

1. **Запуск:** Дважды кликните `JarvisGUI.exe`
2. **Нажмите кнопку:** "▶ Start Jarvis"
3. **Скажите:** "JARVIS, [ваш вопрос]"
4. **Получите ответ:** Голосом и в окне лога

**Примеры команд:**
- "JARVIS, какое сейчас время?"
- "JARVIS, расскажи про Python"
- "JARVIS, открой Google"
- "JARVIS, напиши код для сортировки"

### JarvisCLI (консольная версия)

1. **Запуск:** Дважды кликните `JarvisCLI.exe`
2. **Дождитесь:** "Ассистент готов к работе" 🔊
3. **Скажите:** "JARVIS, [ваш вопрос]"
4. **Получите ответ:** Голосом в динамиках

---

## ⚙️ Вариант 2: Запуск из исходников

### Требования:
- Python 3.8+
- Интернет-соединение

### Установка:

```bash
# 1. Клонируйте репозиторий
git clone <repository-url>
cd local-voice-assistant-byL4ze-

# 2. Создайте виртуальное окружение
python -m venv .venv

# 3. Активируйте
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS

# 4. Установите зависимости
pip install -r requirements.txt
pip install piper-tts

# 5. Создайте .env файл с API ключом
# (см. инструкцию выше)

# 6. Проверьте систему
python verify_setup.py

# 7. Запустите!
python app_gui.py    # GUI версия
# или
python main.py       # CLI версия
```

### Или через скрипты:

```bash
scripts\run.bat         # Универсальный лаунчер
scripts\run_app.bat     # Быстрый запуск GUI
scripts\run_cli.bat     # Быстрый запуск CLI
```

---

## 🔧 Вариант 3: Сборка собственного .exe

### Требования:
- Python 3.8+
- Все зависимости

### Сборка:

```bash
# 1. Запустите скрипт сборки
build.bat

# 2. Найдите результат в папке dist/
dist\JarvisCLI.exe
dist\JarvisGUI.exe
```

**Подробная инструкция:** [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

---

## 🎛️ Настройки

### Изменение голоса
В `.env` файле:
```env
# Для Edge TTS (требует интернет)
TTS_PROVIDER=edge
TTS_VOICE=ru-RU-SvetlanaNeural

# Другие доступные голоса:
# ru-RU-DmitryNeural
# ru-RU-AleksandrNeural
```

### Изменение AI провайдера

#### Groq (по умолчанию, бесплатно)
```env
AI_PROVIDER=groq
GROQ_API_KEY=gsk_xxxxx
GROQ_MODEL=llama-3.3-70b-versatile
```

#### OpenAI (требует API ключ)
```env
AI_PROVIDER=openai
OPEN_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4o-mini
```

#### Локальный AI (Ollama, LM Studio)
```env
AI_PROVIDER=local
LOCAL_AI_URL=http://localhost:11434
LOCAL_AI_MODEL=llama3
```

---

## 🐛 Решение проблем

### ❌ "API key not found" или "Invalid API key"
**Решение:**
1. Убедитесь, что файл `.env` находится в той же папке, что и `.exe`
2. Проверьте, что ключ начинается с `gsk_`
3. Получите новый ключ: https://console.groq.com/keys

### ❌ "No microphone found"
**Решение:**
1. Подключите микрофон/гарнитуру
2. Проверьте в Windows: Settings → Sound → Input
3. Дайте приложению разрешение на использование микрофона

### ❌ Нет звука
**Решение:**
1. Проверьте громкость Windows
2. Убедитесь, что динамики подключены
3. Попробуйте изменить `TTS_PROVIDER=edge` в `.env`

### ❌ Антивирус блокирует .exe
**Решение:**
Это ложное срабатывание (PyInstaller упаковывает Python).
- Добавьте файл в исключения антивируса
- Или используйте запуск из исходников

### ❌ Медленная работа
**Решение:**
1. Измените модель на более быструю: `GROQ_MODEL=llama-3.1-8b-instant`
2. Используйте `TTS_PROVIDER=edge` (быстрее чем Piper)

---

## 📞 Поддержка

- **Документация:** Папка `docs/`
- **Тесты:** Папка `tests/`
- **GitHub Issues:** https://github.com/l4ze-hate/local-voice-assistant-byL4ze-/issues

---

## ✅ Чек-лист готовности

Перед использованием проверьте:
- [ ] `.exe` файл скопирован в рабочую папку
- [ ] Создан файл `.env` с правильным API ключом
- [ ] Микрофон подключен и работает
- [ ] Динамики/наушники подключены
- [ ] Есть интернет-соединение (для Groq API)

---

**Готово! Запустите Jarvis и скажите "JARVIS, привет!" 🎙️🤖**
