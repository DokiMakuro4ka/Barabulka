from bot import bot


@bot.message_handler(commands=["start"])
def handler_command_start(message):
    bot.send_message(chat_id=message.chat.id, text="Привет!")
