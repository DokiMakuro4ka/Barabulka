from bot import bot


@bot.message_handler(content_types=["text"])
def handler_types_text(message):
    if message.text == "Привет!":
        bot.send_message(chat_id=message.chat.id, text="Привет, пупсик ;)")
    else:
        bot.send_message(chat_id=message.chat.id, text=message.text)
