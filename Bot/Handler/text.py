from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, Clas, Subclass


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "👤 Профиль":
        user = User.get_user(message.from_user.id)
        clas = Clas.get_clas(clas_id=user["id_class"])
        subclass = Subclass.get_subclass(subclass_id=user["id_subclass"])

        text = f"""
        Профиль (id{user["id_user"]})\n
        Уровень: {user["lvl"]}
        Опыт: {user["experience_now"]} / {user["experience_future"]}\n
        Класс: {clas["name"]}
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
