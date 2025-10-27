from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "👤 Профиль":
        user = User.get_user(message.from_user.id)
        user_class = UserClass.get_class(class_id=user["class_id"])
        subclass = UserSubclass.get_subclass(subclass_id=user["subclass_id"])

        text = f"""
        Профиль (id{user["user_id"]})\n
        Уровень: {user["lvl"]}
        Опыт: {user["experience_now"]} / {user["experience_future"]}\n
        Класс: {user_class["name"]}
        Подкласс: {subclass["name"]}\n
        Здоровье: {user["hp"]}
        Урон: {user["damage"]}
        Защита: {user["defence"]}
        Ловкость: {user["agility"]}
        Star Коины: {user["star_coin"]}"""

        markup = inline.Profile.profile_1()

        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


    elif message.text == "👨 Капитан":
        bot.send_message(chat_id=message.chat.id, text="В разработке")
