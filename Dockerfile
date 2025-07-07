# Используем официальный базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install flet # Убедитесь, что flet установлен, если его нет в requirements.txt

# Копируем весь ваш проект в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска вашего Flet-приложения
# Cloud Run автоматически установит переменную PORT
CMD ["python", "src/main.py"]