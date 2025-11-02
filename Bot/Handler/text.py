from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass, UserState


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "👤 Профиль":
        user = User.get_user(message.from_user.id)
        user_class = UserClass.get_class(class_id=user["class_id"])
        user_subclass = UserSubclass.get_subclass(subclass_id=user["subclass_id"])
        user_state = UserState.get_state(state_id=user["state_id"])

        text = f"""
        Профиль (id{user["user_id"]})
        Имя: {user["name"]}
        Государство: {user_state["name"]}\n
        Уровень: {user["lvl"]}
        Опыт: {user["experience_now"]} / {user["experience_future"]}\n
        Класс: {user_class["name"]}
        Подкласс: {user_subclass["name"]}\n
        Здоровье: {user["hp"]}
        Урон: {user["damage"]}
        Защита: {user["defence"]}
        Ловкость: {user["agility"]}
        Очки навыков: {user["skill_point"]}
        Star Коины: {user["star_coin"]}"""

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
