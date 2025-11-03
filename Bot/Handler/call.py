from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass, UserState



@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):

    ################################# ВСТУПЛЕНИЕ #################################

    if call.data == "state_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии. Теперь ведут войны между собой в жажде власти!\n\nВыберите Государство:"
        markup = inline.Plot.introduction_state_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание <Государства 1>, лор этой страны. Плюсы и минусы"
        markup = inline.Plot.introduction_state_description_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание <Государства 2>, лор этой страны. Плюсы и минусы"
        markup = inline.Plot.introduction_state_description_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание <Государства 3>, лор этой страны. Плюсы и минусы"
        markup = inline.Plot.introduction_state_description_3()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        photo_path = "C:\IT\Barabulka\Picture\kingdom_dwarves.png"
        state = UserState.get_state(state_id=4)
        text = f"{state["description"]}\n\n" \
               f"Бафы, плюсы:\n" \
               f"- 1 - Плюс 5% к здоровью\n" \
               f"- 2 - Урон по ассасинам на 5% больше.\n\n" \
               f"Дебафы, минусы:\n" \
               f"- 1 - Передвижение между локациями на 20% больше;\n" \
               f"- 2 - Урон по магам на 10% меньше."
        markup = inline.Plot.introduction_state_description_4()
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id=call.message.chat.id, photo=photo_file, caption=text, reply_markup=markup)


    elif call.data == "select_state_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Вы выбрали государство <Государство 1>."
        User.insert_user(user_id=call.from_user.id, state_id=1)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_state_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Вы выбрали государство <Государство 2>."
        User.insert_user(user_id=call.from_user.id, state_id=2)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_state_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Вы выбрали государство <Государство 3>."
        User.insert_user(user_id=call.from_user.id, state_id=3)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_state_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Вы выбрали государство <Государство 4>."
        User.insert_user(user_id=call.from_user.id, state_id=4)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "class_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Бла бла бла, ты нам нужен. Как ты препочитаешь драться в бою.\n\nВыберите класс:"
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
        text = f"Ты выбрал класс <Маг>."
        User.set_user_class_id(user_id=call.from_user.id, class_id=1)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Рыцарь>."
        User.set_user_class_id(user_id=call.from_user.id, class_id=2)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Лучник>."
        User.set_user_class_id(user_id=call.from_user.id, class_id=3)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Ты выбрал класс <Ассасин>."
        User.set_user_class_id(user_id=call.from_user.id, class_id=4)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    ################################# КНОПКИ В БЫСТРОЙ ПАНАЛИ #################################

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
        user = User.get_user(call.from_user.id)
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
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(call.from_user.id)
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
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
