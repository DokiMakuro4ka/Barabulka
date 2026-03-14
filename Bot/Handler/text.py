from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass, UserState
from Bot.utils.messages import send_and_track_message


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "👤 Профиль":
        text = User.get_user_text(user_id=message.chat.id)
        markup = inline.Profile.profile_1()
        send_and_track_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup,
        )

    elif message.text == "👨 Капитан":
        user = User.get_user(message.from_user.id)

        if user is None:
            send_and_track_message(
                chat_id=message.chat.id,
                text="Сначала нажми /start, чтобы зарегистрироваться.",
            )
            return

        if user["class_id"] == 0:
            markup = inline.Plot.introduction_class_selection()
            text = (
                "Бла бла бла, ты нам нужен. Как ты предпочитаешь драться в бою.\n\n"
                "Выберите класс:"
            )
            send_and_track_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=markup,
            )
        else:
            send_and_track_message(
                chat_id=message.chat.id,
                text="В разработке",
            )