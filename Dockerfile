# Укажите базовый образ
FROM python:3.10

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Откройте порт для приложения
EXPOSE 8000

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
