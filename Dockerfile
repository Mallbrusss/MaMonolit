# Используем официальный образ Python 3.12
FROM python:3.12

# Устанавливаем необходимые системные пакеты (если нужны)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию для приложения внутри контейнера
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения в контейнер
COPY . /app/

# Экспортируем переменные окружения (если нужно)
# ENV VARIABLE_NAME=value

# Указываем команду запуска приложения
CMD ["streamlit", "run", "app.py","--server.port=8501","--server.address=0.0.0.0"]