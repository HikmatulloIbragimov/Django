# 1. Базовый Python-образ
FROM python:3.11-slim

# 2. Обновляем и устанавливаем ffmpeg + PostgreSQL драйвер + компилятор
RUN apt-get update && \
    apt-get install -y ffmpeg libpq-dev gcc && \
    apt-get clean

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Копируем проект в контейнер
COPY . /app

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Запуск gunicorn (замени `myproject` на имя твоего проекта, если другое)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
