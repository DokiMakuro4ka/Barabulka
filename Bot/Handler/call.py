from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass, UserState, State



@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):

    ################################# ВСТУПЛЕНИЕ #################################

    if call.data == "state_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии. Теперь ведут войны между собой в жажде власти!\n\nВыберите Государство:"
        markup = inline.Plot.introduction_state_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    #+++++++++++++++++++++++++++++++ГОСУДАРСТВО АЙКАТЦУ+++++++++++++++++++++++++++++++#
    elif call.data == "state_selection_aikatsu":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Айкацу — это парящее государство, расположенное на цепи летающих островов, соединённых мостами из ветра и облаков. Его жители — мастера магии воздуха, дисциплины и чести. Культура Айкацу сочетает духовные практики, боевые искусства и строгий кодекс, напоминающий бусидо самураев. Здесь магия — не просто сила, а путь к просветлению"
        markup = inline.Plot.introduction_state_aikatsu()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    
    #- - - - - - - - - - - - -  ЭПОХИ ГОСУДАРСТВА АЙКАЦУ  - - - - - - - - - - - - - -# 
    #--------------------------------ЭПОХА ТУМАНА-------------------------------#
    elif call.data == "The_Age_of_Fog":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Когда-то Айкацу был разрозненным архипелагом из парящих островов, каждый из которых принадлежал отдельному клану. Эти кланы веками развивали собственные школы магии воздуха, не признавая чужих традиций. Магия была не путём просветления, а оружием — кланы сражались за контроль над потоками ветра, небесными артефактами и стратегическими воздушными маршрутами."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    
    ##------------------------ ПОДРОБНОСТИ ПРО ЭПОХУ ТУМАНА -----------------------##
    # ⚔️ Конфликты в эпоху тумана
    elif call.data == "conflicts_The_Age_of_Fog":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Войны за облачные артефакты: древние реликвии, усиливающие магию, становились причиной кровопролитных сражений.\n\n" \
               f"Потоки ветра: магические каналы между островами — контроль над ними означал власть.\n\n" \
               f"Изоляция школ: каждая школа магии считала себя единственно верной, что порождало фанатизм и закрытость."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    # 🌫️ Культура в эпоху тумана
    elif call.data == "Culture_The_Age_of_Fog":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Магия передавалась по крови и тайным ритуалам.\n\n" \
               f"Кланы строили храмы на вершинах облаков, недоступные для чужаков.\n\n" \
               f"Появились легенды о Долине Природы — месте, где все стихии равны, но никто не мог её найти."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #--------------------------------ЭПОХА ОБЪЕДИНЕНИЯ-------------------------------#
    elif call.data == "The_Era_of_Unification":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Великий маг-самурай Хосэи, родом из клана Сэйка, стал первым, кто осознал, что разрозненность ведёт к гибели. Он объединил кланы, победив Бурю Раздора — магический катаклизм, вызванный конфликтом стихий. Хосэи предложил новый путь: магия как дисциплина, а не как оружие."
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    ##------------------------ ПОДРОБНОСТИ ПРО ЭПОХУ ОБЪЕДИНЕНИЯ -----------------------##
    # 📜 Кодекс Воздушного Пути
    elif call.data == "The_Era_of_Unification_The_Code_of_the_Air_Path":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Хосэи создал свод правил, сочетающий магию и самурайскую этику. Кодекс включал: \n\n" \
               f"1) Чистоту Намерения \n\n" \
               f"2) Тишину Сердца \n\n" \
               f"3) Силу Без Гнева \n\n" \
               f"4) Путь Ветра \n\n" \
               f"5) Честь Движения \n\n" \
               f"6) Защиту Слабого \n\n" \
               f"7) Гармонию Стихий" 
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    # 🏛️ Небесный Додзё
    elif call.data == "The_Era_of_Unification_The_Celestial_Dojo":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"На центральном острове был построен храм, где обучали четырём путям: \n\n" \
               f"Клинок (Фуусин) \n\n" \
               f"Дыхание (Камино) \n\n" \
               f"Туман (Кагэноха) \n\n" \
               f"Щит (Сораносеки) "
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    # 🤝 Последствия
    elif call.data == "The_Era_of_Unification_The_Consequences":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Кланы сохранили свои школы, но приняли общую структуру. \n\n" \
               f"Магия стала инструментом баланса. \n\n" \
               f"Началась эпоха дипломатии и духовного роста. "
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    
    #--------------------------------ЭПОХА ПАРЯЩИХ ВРАТ-------------------------------#
    elif call.data == "The_Age_of_Floating_Gates":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание <Государства 1>, лор этой страны. Плюсы и минусы"
        markup = inline.Plot.introduction_state_description_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = UserState.get_state(state_id=2)
        text = f"{state["description"]}\n\n" \
               f"Бафы, плюсы:\n" \
               f"- 1 - \n" \
               f"- 2 - \n\n" \
               f"Дебафы, минусы:\n" \
               f"- 1 - \n" \
               f"- 2 - "
        markup = inline.Plot.introduction_state_description_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = UserState.get_state(state_id=3)
        text = f"{state["description"]}\n\n" \
               f"Бафы, плюсы:\n" \
               f"- 1 - \n" \
               f"- 2 - \n\n" \
               f"Дебафы, минусы:\n" \
               f"- 1 - \n" \
               f"- 2 - "
        markup = inline.Plot.introduction_state_description_3()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "state_selection_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        photo_path = "C:\IT\Barabulka\Picture\kingdom_dwarves.png"
        state = UserState.get_state(state_id=4)
        text = f"{state["description"]}\n\n" \
               f"Бафы, плюсы:\n" \
               f"- 1 - Плюс 5% к здоровью\n" \
               f"- 2 - Урон по ассасинам на 5% больше\n\n" \
               f"Дебафы, минусы:\n" \
               f"- 1 - Передвижение между локациями на 20% больше\n" \
               f"- 2 - Урон по магам на 10% меньше"
        markup = inline.Plot.introduction_state_description_4()
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id=call.message.chat.id, photo=photo_file, caption=text, reply_markup=markup)


    elif call.data == "select_state_aikatsu":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = f"Вы выбрали государство Айкацу."
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
        state = State.get_state(state_id=4)
        text = f"Вы выбрали государство: {state["name"]}. Подойдите к капитану он введет в курс дела."
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
        text = f"""Тут должно быть описание класса {user_class["name"]}"""
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

    elif call.data == "profile_class_back" or call.data == "profile_subclass_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = User.get_user_text(user_id=call.from_user.id)
        markup = inline.Profile.profile_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)