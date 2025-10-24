from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, Clas, Subclass


@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):
    if call.data == "class_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "class_selection_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Маг>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Рыцарь>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Описание класса <Лучник>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."""
        markup = inline.Plot.introduction_class_description_3()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Описание класса <Ассасин>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_4()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "select_class_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Маг>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=1)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Рыцарь>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=2)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Лучник>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=3)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Ассасин>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=4)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "profile_class":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
        clas = Clas.get_clas(clas_id=user["id_class"])
        text = f"Тут должно быть описание класса {clas["name"]}"
        markup = inline.Profile.profile_class()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_class_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(call.from_user.id)
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
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
        subclass = Subclass.get_subclass(subclass_id=user["id_subclass"])
        if subclass["id_subclass"] == 0:
            text = f"У тебя нету подкласса.\nЧто-бы его получить. Подойти к ментору, по достяжению 25 уровня."
        else:
            pass
        markup = inline.Profile.profile_subclass()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(call.from_user.id)
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
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_skills":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")

    elif call.data == "profile_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
