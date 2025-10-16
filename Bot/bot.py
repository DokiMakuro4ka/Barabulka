import telebot
from dotenv import load_dotenv
import os


# Загрузка переменных из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Иницилизация бота
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
