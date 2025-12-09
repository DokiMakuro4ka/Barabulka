from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User, UserClass, UserSubclass, UserState, State, Epoch, EpochDetail
import os


@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):

    ################################# ВСТУПЛЕНИЕ #################################

    if call.data == "state_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Четыре силы, некогда хранители гармонии. "
            "Теперь ведут войны между собой в жажде власти!\n\n"
            "Выберите Государство:"
        )
        markup = inline.Plot.introduction_state_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #+++++++++++++++++++++++++++++++ГОСУДАРСТВО АЙКАЦУ+++++++++++++++++++++++++++++++#

    elif call.data == "state_selection_aikatsu":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = State.get_state_by_name("Айкацу")
        text = state["description"] if state and state.get("description") else "Описание не найдено."
        markup = inline.Plot.introduction_state_aikatsu()

        photo_path = r"C:\Users\Doki\Documents\OldWin\projects\Barabulka\Picture\state_Aikatsu.png"
        if os.path.exists(photo_path):
            with open(photo_path, "rb") as photo_file:
                bot.send_photo(chat_id=call.message.chat.id, photo=photo_file, caption=text, reply_markup=markup)
        else:
            bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #- - - - - - - - - - - - - ЭПОХИ ГОСУДАРСТВА АЙКАЦУ - - - - - - - - - - - - - -#

    #--------------------------------ЭПОХА ТУМАНА-------------------------------#

    elif call.data == "The_Age_of_Fog":
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        text = epoch["description"] if epoch and epoch.get("description") else "Эпоха не найдена."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    ##------------------------ ПОДРОБНОСТИ ПРО ЭПОХУ ТУМАНА -----------------------##

    # ⚔️ Конфликты в эпоху тумана

    elif call.data == "conflicts_The_Age_of_Fog":
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        if epoch:
            detail = EpochDetail.get_detail_by_category(epoch["epoch_id"], "Конфликты")
            text = detail["content"] if detail and detail.get("content") else "Деталь не найдена."
        else:
            text = "Эпоха не найдена."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    # 🌫️ Культура в эпоху тумана

    elif call.data == "Culture_The_Age_of_Fog":
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        if epoch:
            detail = EpochDetail.get_detail_by_category(epoch["epoch_id"], "Культура")
            text = detail["content"] if detail and detail.get("content") else "Деталь не найдена."
        else:
            text = "Эпоха не найдена."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #--------------------------------ЭПОХА ОБЪЕДИНЕНИЯ-------------------------------#

    elif call.data == "The_Era_of_Unification":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Великий маг-самурай Хосэй, родом из клана Сэйка, стал первым, кто осознал, "
            "что разрозненность ведёт к гибели. Он объединил кланы, победив Бурю Раздора — "
            "магический катаклизм, вызванный конфликтом стихий. Хосэй предложил новый путь: "
            "магия как дисциплина, а не как оружие."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    ##------------------------ ПОДРОБНОСТИ ПРО ЭПОХУ ОБЪЕДИНЕНИЯ -----------------------##

    # 📜 Кодекс Воздушного Пути

    elif call.data == "The_Era_of_Unification_The_Code_of_the_Air_Path":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Хосэй создал свод правил, сочетающий магию и самурайскую этику. Кодекс включал:\n\n"
            "1) Чистоту Намерения\n\n"
            "2) Тишину Сердца\n\n"
            "3) Силу Без Гнева\n\n"
            "4) Путь Ветра\n\n"
            "5) Честь Движения\n\n"
            "6) Защиту Слабого\n\n"
            "7) Гармонию Стихий"
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    # 🏛️ Небесный Додзё

    elif call.data == "The_Era_of_Unification_The_Celestial_Dojo":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "На центральном острове был построен храм, где обучали четырём путям:\n\n"
            "Клинок (Фуусин)\n\n"
            "Дыхание (Камино)\n\n"
            "Туман (Кагэноха)\n\n"
            "Щит (Сораносеки)"
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    # 🤝 Последствия

    elif call.data == "The_Era_of_Unification_The_Consequences":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Кланы сохранили свои школы, но приняли общую структуру.\n\n"
            "Магия стала инструментом баланса.\n\n"
            "Началась эпоха дипломатии и духовного роста."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #--------------------------------ЭПОХА ПАРЯЩИХ ВРАТ-------------------------------#

    elif call.data == "The_Age_of_Floating_Gates":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Айкацу стал центром воздушной магии. Его мастера уважаемы во всех государствах. "
            "Развились воздушные технологии: парящие библиотеки, храмы, мосты из ветра."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    ##------------------------ ПОДРОБНОСТИ ПРО ЭПОХУ ПАРЯЩИХ ВРАТ -----------------------##

    # ⚠️ Внешние угрозы

    elif call.data == "The_Age_of_Floating_Gates_External_threats":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Государства Огня и Земли стремятся проникнуть в Долину Природы, "
            "чтобы овладеть её силой.\n\n"
            "Айкацу защищает Долину, считая её священным источником равновесия."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    # 💥 Внутренний конфликт

    elif call.data == "The_Age_of_Floating_Gates_Internal_conflict":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Традиционалисты: верны Кодексу, считают, что магия — путь к просветлению.\n\n"
            "Новаторы: хотят использовать магию для прогресса, создания оружия, изменения Кодекса."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    # 🧩 Политическая напряжённость

    elif call.data == "The_Age_of_Floating_Gates_Political_tension":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Совет Айкацу расколот: часть поддерживает реформы, часть — возвращение к философии Хосэя.\n\n"
            "Появляются тайные школы, нарушающие Кодекс.\n\n"
            "Некоторые маги начинают искать альтернативные пути, включая союз с другими стихиями."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #--------------------------------ГОСУДАРСТВО 2-------------------------------#

    elif call.data == "state_selection_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = UserState.get_state(state_id=2)
        desc = state["description"] if state and state.get("description") else "Описание не найдено."
        text = (
            f"{desc}\n\n"
            "Бафы, плюсы:\n"
            "- 1 -\n"
            "- 2 -\n\n"
            "Дебафы, минусы:\n"
            "- 1 -\n"
            "- 2 -"
        )
        markup = inline.Plot.introduction_state_description_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #--------------------------------ГОСУДАРСТВО 3-------------------------------#

    elif call.data == "state_selection_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = UserState.get_state(state_id=3)
        desc = state["description"] if state and state.get("description") else "Описание не найдено."
        text = (
            f"{desc}\n\n"
            "Бафы, плюсы:\n"
            "- 1 -\n"
            "- 2 -\n\n"
            "Дебафы, минусы:\n"
            "- 1 -\n"
            "- 2 -"
        )
        markup = inline.Plot.introduction_state_description_3()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #--------------------------------ГОСУДАРСТВО 4-------------------------------#

    elif call.data == "state_selection_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = UserState.get_state(state_id=4)
        desc = state["description"] if state and state.get("description") else "Описание не найдено."
        text = (
            f"{desc}\n\n"
            "Бафы, плюсы:\n"
            "- 1 - Плюс 5% к здоровью\n"
            "- 2 - Урон по ассасинам на 5% больше\n\n"
            "Дебафы, минусы:\n"
            "- 1 - Передвижение между локациями на 20% больше\n"
            "- 2 - Урон по магам на 10% меньше"
        )
        markup = inline.Plot.introduction_state_description_4()

        photo_path = r"C:\Users\Doki\Documents\OldWin\projects\Barabulka\Picture\kingdom_dwarves.png"
        if os.path.exists(photo_path):
            with open(photo_path, "rb") as photo_file:
                bot.send_photo(chat_id=call.message.chat.id, photo=photo_file, caption=text, reply_markup=markup)
        else:
            bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #++++++++++++++++++++++++++++++++ ВЫБОР ГОСУДАРСТВА ++++++++++++++++++++++++++++++#

    elif call.data == "select_state_aikatsu":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Вы выбрали государство Айкацу."
        User.insert_user(user_id=call.from_user.id, state_id=1)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_state_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Вы выбрали государство <Государство 2>."
        User.insert_user(user_id=call.from_user.id, state_id=2)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_state_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Вы выбрали государство <Государство 3>."
        User.insert_user(user_id=call.from_user.id, state_id=3)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_state_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        state = State.get_state(state_id=4)
        name = state["name"] if state and state.get("name") else "Неизвестное государство"
        text = f"Вы выбрали государство: {name}. Подойдите к капитану, он введёт вас в курс дела."
        User.insert_user(user_id=call.from_user.id, state_id=4)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #++++++++++++++++++++++++++++++++ ВЫБОР КЛАССА ++++++++++++++++++++++++++++++#

    elif call.data == "class_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Бла бла бла, ты нам нужен. Как ты предпочитаешь драться в бою?\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Описание класса <Маг>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Описание класса <Рыцарь>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Описание класса <Лучник>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_3()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = (
            "Описание класса <Ассасин>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_4()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    #++++++++++++++++++++++++++++++++ ПОДТВЕРЖДЕНИЕ КЛАССА ++++++++++++++++++++++++++++++#

    elif call.data == "select_class_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Маг>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=1)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Рыцарь>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=2)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Лучник>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=3)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Ассасин>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=4)
        markup = reply.Plot.introduction_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    ################################# КНОПКИ В БЫСТРОЙ ПАНЕЛИ #################################

    elif call.data == "profile_class":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
        if user and user.get("class_id"):
            user_class = UserClass.get_class(class_id=user["class_id"])
            class_name = user_class["name"] if user_class and user_class.get("name") else "Неизвестный класс"
            text = f"Тут должно быть описание класса {class_name}"
        else:
            text = "Класс не выбран."
        markup = inline.Profile.profile_class()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        user = User.get_user(user_id=call.from_user.id)
        if user and user.get("subclass_id") and user["subclass_id"] != 0:
            subclass = UserSubclass.get_subclass(subclass_id=user["subclass_id"])
            if subclass and subclass.get("name"):
                text = f"Тут должно быть описание подкласса {subclass['name']}"
            else:
                text = "Описание подкласса недоступно."
        else:
            text = "У тебя нету подкласса.\nЧтобы его получить, подойди к ментору по достижении 25 уровня."
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
        # добавить нужный код возврата в главное меню
