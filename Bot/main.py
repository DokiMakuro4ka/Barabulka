import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os


# Загрузка переменных из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Иницилизация бота
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
print("----- БОТ ЗАПУЩЕН -----")


# Основной код
@bot.message_handler(commands=["start"])
def handler_command_start(message):
    bot.send_message(chat_id=message.chat.id, text="Привет!")


bot.infinity_polling()
