from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User


@bot.message_handler(commands=["start"])
def handler_command_start(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)

    user = User.get_user(message.from_user.id)

    if user is None:
        text = f"Тьма окутала Долину Природы, как бездонная ночь. Реки, некогда сиявшие золотом, застынули в ледяной тишине. Деревья стояли безмолвные, цветы — опавшие лепестки под тяжестью горя. Ветер приносил лишь крики разрушенных земель."
        markup = inline.Plot.introduction_lor()
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


    else:
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=message.chat.id, text="Ты уже зарегистрирован", reply_markup=markup)
