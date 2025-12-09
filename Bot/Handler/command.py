from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User


@bot.message_handler(commands=["start"])
def handler_command_start(message):
    user = User.get_user(message.from_user.id)

    if user is None:
        photo_path = "Picture\lor.png"
        text = f"Тьма окутала Долину Природы, как бездонная ночь. Реки, некогда сиявшие золотом, застынули в ледяной тишине. Деревья стояли безмолвные, цветы — опавшие лепестки под тяжестью горя. Ветер приносил лишь крики разрушенных земель."
        markup = inline.Plot.introduction_lor()
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id=message.chat.id, photo=photo_file, caption=text, reply_markup=markup)


    else:
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=message.chat.id, text="Ты уже зарегистрирован", reply_markup=markup)
