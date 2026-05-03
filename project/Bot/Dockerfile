FROM python:3.12-slim

WORKDIR /app

# Копируем requirements.txt из текущей папки (предварительно скопируйте его туда)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бота
COPY . .

CMD ["python", "main.py"]