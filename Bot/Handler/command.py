from Bot.bot import bot
from Bot.Keyboard import inline


@bot.message_handler(commands=["start"])
def handler_command_start(message):
    text = f"Тьма окутала Долину Природы, как бездонная ночь. Реки, некогда сиявшие золотом, застынули в ледяной тишине. Деревья стояли безмолвные, цветы — опавшие лепестки под тяжестью горя. Ветер приносил лишь крики разрушенных земель."
    markup = inline.Plot.introduction_1()
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
