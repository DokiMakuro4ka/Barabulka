from Bot.bot import bot
from Bot.Keyboard import inline


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "👤 Профиль":
        bot.send_message(chat_id=message.chat.id, text="В разработке")
    
    elif message.text == "👨 Капитан":
        bot.send_message(chat_id=message.chat.id, text="В разработке")
