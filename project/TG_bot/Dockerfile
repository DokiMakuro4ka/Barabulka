FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости (requirements.txt) из TG_bot (если есть) или из корня
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бота
COPY . .

CMD ["python", "main.py"]