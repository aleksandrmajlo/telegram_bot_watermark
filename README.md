# Telegram Bot Watermark

Простой бот на Python, который:
- Получает фото из Telegram
- Добавляет водяной знак (лого)
- Сохраняет или отправляет обратно

---

## 📦 Структура проекта

```
telegram_bot_watermark/
├── bot/
│   ├── init.py
│   ├── handlers.py
│   ├── photo_processor.py
│   ├── watermark_manager.py
├── service/
│   ├── init.py
│   ├── watermark_photo.py
│   ├── watermark_video.py
├── watermark/
│   ├── logo.png
│   ├── logo_48.png
│   ├── logo_video.png
├── venv/                # виртуальное окружение
├── .env                 # переменные окружения
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
```

---

## ⚙ Настройка

1️⃣ Установите Python 3.

2️⃣ Клонируйте репозиторий (или скачайте папку).

3️⃣ Создайте файл `.env` в корне проекта:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
LOGO_PATH=watermark/logo.png
LOGO_VIDEO_PATH=watermark/logo_video.png
```

---

## 🏗 Установка и запуск

### Linux/macOS

```bash
# 1. Создаём виртуальное окружение
python3 -m venv venv

# 2. Активируем окружение
source venv/bin/activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Запускаем скрипт
python main.py

# 5. (После работы) Деактивируем окружение
deactivate
```

---

### Windows (cmd)

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
deactivate
```

---

## 💡 Что делает скрипт

- Получает `file_id` из Telegram 
- Скачивает фото
- Добавляет на фото водяной знак (размер автоматически масштабируется)
- Сохраняет файл как `output.jpg`
- (Опционально) Отправляет его обратно в чат

---

## 📋 TODO (что можно улучшить)

✅ Добавить Flask/FastAPI webhook  
✅ Добавить Dockerfile  
✅ Добавить unit-тесты  
✅ Обработку ошибок и логирование  
✅ Удаление временных файлов

---



---

**Автор:** 🚀 aleksandrmajlo@gmail.com