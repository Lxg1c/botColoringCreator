# Используем официальный образ Python
FROM python:3.13

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt requirements.txt
# Устанавлием инструмент для компилирования зависимсотей
RUN pip install --upgrade setuptools

# Устанавливаем зависомости
RUN pip install -r requirements.txt

# Устанавилем уровень доступа
RUN chmod 755 .

# Копируем исходный код
COPY . .

# Команда для запуска бота
CMD ["python", "-m", "main"]