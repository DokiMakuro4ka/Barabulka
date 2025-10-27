from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass



@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):
    if call.data == "class_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "class_selection_mage":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Маг>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_mage()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_knight":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Рыцарь>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_knight()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_archer":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Описание класса <Лучник>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."""
        markup = inline.Plot.introduction_class_description_archer()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_assassin":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Описание класса <Ассасин>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_assassin()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "select_class_mage":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Маг>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=1)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_knight":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Рыцарь>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=2)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_archer":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Лучник>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=3)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_assassin":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Ассасин>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=4)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "profile_class":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
        user_class = UserClass.get_class(class_id=user["class_id"])
        text = f"Тут должно быть описание класса {user_class["name"]}"
        markup = inline.Profile.profile_class()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
        subclass = UserSubclass.get_subclass(subclass_id=user["subclass_id"])
        if subclass["subclass_id"] == 0:
            text = f"У тебя нету подкласса.\nЧто-бы его получить. Подойти к ментору, по достяжению 25 уровня."
        else:
            pass
        markup = inline.Profile.profile_subclass()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_skills":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")

    elif call.data == "profile_class_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
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
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
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
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
