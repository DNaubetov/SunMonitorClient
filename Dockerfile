# Используем минимальный образ с Python
FROM python:3.12.4-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Копируем код приложения в контейнер
COPY . /app

# Устанавливаем переменные окружения через .env
ENV PYTHONUNBUFFERED=1

# Запускаем приложение
CMD ["python", "main.py"]
