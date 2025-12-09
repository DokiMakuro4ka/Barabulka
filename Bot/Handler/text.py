from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass, UserState


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "👤 Профиль":
        text = User.get_user_text(user_id=message.chat.id)
        markup = inline.Profile.profile_1()
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


    elif message.text == "👨 Капитан":
        user = User.get_user(message.from_user.id)
        if user["class_id"] == 0:
            markup = inline.Plot.introduction_class_selection()
            text = "Бла бла бла, ты нам нужен. Как ты препочитаешь драться в бою.\n\nВыберите класс:"
            bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
        else:
            bot.send_message(chat_id=message.chat.id, text="В разработке")
