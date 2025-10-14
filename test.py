import telebot
import api_key

bot = telebot.TeleBot(api_key.KEY)

@bot.message_handler(commands=['start'])
def main (message):
    bot.send_message(message.chat.id, message.from_user.id)

bot.infinity_polling()