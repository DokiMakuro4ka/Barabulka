FROM python:3.14-slim

WORKDIR /app

# Ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (включая Picture, Bot, app.py и т.д.)
COPY . .

# Точка входа бота
CMD ["python", "app.py"]
