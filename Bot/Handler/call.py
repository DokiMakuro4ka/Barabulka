import os
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout, SSLError
from telebot.apihelper import ApiTelegramException

from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import (
    User,
    UserClass,
    UserSubclass,
    UserState,
    State,
    Epoch,
    EpochDetail,
)

load_dotenv()

STATE_AIKATSU_PHOTO_ID = os.getenv("START_PHOTO_ID_AIKATSU")
KINGDOM_DWARVES_PHOTO_ID = os.getenv("START_PHOTO_ID_DWARVES")

PHOTO_IDS = {
    "aikatsu": STATE_AIKATSU_PHOTO_ID,
    "dwarves": KINGDOM_DWARVES_PHOTO_ID,
}

LAST_BOT_MESSAGES = {}


def delete_tracked_message(chat_id):
    message_id = LAST_BOT_MESSAGES.get(chat_id)
    if not message_id:
        return

    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print("delete_tracked_message error:", repr(e))
    finally:
        LAST_BOT_MESSAGES.pop(chat_id, None)


def delete_current_callback_message(call):
    chat_id = call.message.chat.id
    message_id = call.message.id

    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print("delete_current_callback_message error:", repr(e))
    finally:
        if LAST_BOT_MESSAGES.get(chat_id) == message_id:
            LAST_BOT_MESSAGES.pop(chat_id, None)


def send_and_track_message(chat_id, text, reply_markup=None):
    delete_tracked_message(chat_id)
    msg = bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
    )
    LAST_BOT_MESSAGES[chat_id] = msg.message_id
    return msg


def send_and_track_photo(chat_id, photo_id, caption, reply_markup=None, fallback_text=None):
    delete_tracked_message(chat_id)

    try:
        msg = bot.send_photo(
            chat_id=chat_id,
            photo=photo_id,
            caption=caption,
            reply_markup=reply_markup,
        )
        LAST_BOT_MESSAGES[chat_id] = msg.message_id
        return msg
    except (ApiTelegramException, ConnectionError, Timeout, SSLError, OSError) as e:
        print("send_photo error:", repr(e))
        msg = bot.send_message(
            chat_id=chat_id,
            text=fallback_text or caption,
            reply_markup=reply_markup,
        )
        LAST_BOT_MESSAGES[chat_id] = msg.message_id
        return msg


@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):
    chat_id = call.message.chat.id

    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        print("answer_callback_query error:", repr(e))

    ################################# ВСТУПЛЕНИЕ #################################

    if call.data == "state_selection":
        delete_current_callback_message(call)
        text = (
            "Четыре силы, некогда хранители гармонии. "
            "Теперь ведут войны между собой в жажде власти!\n\n"
            "Выберите Государство:"
        )
        markup = inline.Plot.introduction_state_selection()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # +++++++++++++++++++++++++++++++ ГОСУДАРСТВО АЙКАЦУ +++++++++++++++++++++++++++++++

    elif call.data == "state_selection_aikatsu":
        delete_current_callback_message(call)
        state = State.get_state_by_name("Айкацу")
        text = state["description"] if state and state.get("description") else "Описание не найдено."
        markup = inline.Plot.introduction_state_aikatsu()

        photo_id = PHOTO_IDS["aikatsu"]
        if photo_id:
            send_and_track_photo(
                chat_id=chat_id,
                photo_id=photo_id,
                caption=text,
                reply_markup=markup,
                fallback_text=text,
            )
        else:
            send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Age_of_Fog":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        text = epoch["description"] if epoch and epoch.get("description") else "Эпоха не найдена."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "conflicts_The_Age_of_Fog":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        if epoch:
            detail = EpochDetail.get_detail_by_category(epoch["epoch_id"], "Конфликты")
            text = detail["content"] if detail and detail.get("content") else "Деталь не найдена."
        else:
            text = "Эпоха не найдена."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "Culture_The_Age_of_Fog":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        if epoch:
            detail = EpochDetail.get_detail_by_category(epoch["epoch_id"], "Культура")
            text = detail["content"] if detail and detail.get("content") else "Деталь не найдена."
        else:
            text = "Эпоха не найдена."
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Fog()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Era_of_Unification":
        delete_current_callback_message(call)
        text = (
            "Великий маг-самурай Хосэй, родом из клана Сэйка, стал первым, кто осознал, "
            "что разрозненность ведёт к гибели. Он объединил кланы, победив Бурю Раздора — "
            "магический катаклизм, вызванный конфликтом стихий. Хосэй предложил новый путь: "
            "магия как дисциплина, а не как оружие."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Era_of_Unification_The_Code_of_the_Air_Path":
        delete_current_callback_message(call)
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
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Era_of_Unification_The_Celestial_Dojo":
        delete_current_callback_message(call)
        text = (
            "На центральном острове был построен храм, где обучали четырём путям:\n\n"
            "Клинок (Фуусин)\n\n"
            "Дыхание (Камино)\n\n"
            "Туман (Кагэноха)\n\n"
            "Щит (Сораносеки)"
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Era_of_Unification_The_Consequences":
        delete_current_callback_message(call)
        text = (
            "Кланы сохранили свои школы, но приняли общую структуру.\n\n"
            "Магия стала инструментом баланса.\n\n"
            "Началась эпоха дипломатии и духовного роста."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Era_of_Unification()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Age_of_Floating_Gates":
        delete_current_callback_message(call)
        text = (
            "Айкацу стал центром воздушной магии. Его мастера уважаемы во всех государствах. "
            "Развились воздушные технологии: парящие библиотеки, храмы, мосты из ветра."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Age_of_Floating_Gates_External_threats":
        delete_current_callback_message(call)
        text = (
            "Государства Огня и Земли стремятся проникнуть в Долину Природы, "
            "чтобы овладеть её силой.\n\n"
            "Айкацу защищает Долину, считая её священным источником равновесия."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Age_of_Floating_Gates_Internal_conflict":
        delete_current_callback_message(call)
        text = (
            "Традиционалисты: верны Кодексу, считают, что магия — путь к просветлению.\n\n"
            "Новаторы: хотят использовать магию для прогресса, создания оружия, изменения Кодекса."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "The_Age_of_Floating_Gates_Political_tension":
        delete_current_callback_message(call)
        text = (
            "Совет Айкацу расколот: часть поддерживает реформы, часть — возвращение к философии Хосэя.\n\n"
            "Появляются тайные школы, нарушающие Кодекс.\n\n"
            "Некоторые маги начинают искать альтернативные пути, включая союз с другими стихиями."
        )
        markup = inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # -------------------------------- ГОСУДАРСТВО 2 -------------------------------

    elif call.data == "state_selection_2":
        delete_current_callback_message(call)
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
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # -------------------------------- ГОСУДАРСТВО 3 -------------------------------

    elif call.data == "state_selection_3":
        delete_current_callback_message(call)
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
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # -------------------------------- ГОСУДАРСТВО ДВАРФОВ -------------------------------

    elif call.data == "state_selection_4":
        delete_current_callback_message(call)
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

        photo_id = PHOTO_IDS["dwarves"]
        if photo_id:
            send_and_track_photo(
                chat_id=chat_id,
                photo_id=photo_id,
                caption=text,
                reply_markup=markup,
                fallback_text=text,
            )
        else:
            send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # ++++++++++++++++++++++++++++++++ ВЫБОР ГОСУДАРСТВА ++++++++++++++++++++++++++++++

    elif call.data == "select_state_aikatsu":
        delete_current_callback_message(call)
        text = "Вы выбрали государство Айкацу."
        User.insert_user(user_id=call.from_user.id, state_id=1)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_state_2":
        delete_current_callback_message(call)
        text = "Вы выбрали государство <Государство 2>."
        User.insert_user(user_id=call.from_user.id, state_id=2)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_state_3":
        delete_current_callback_message(call)
        text = "Вы выбрали государство <Государство 3>."
        User.insert_user(user_id=call.from_user.id, state_id=3)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_state_4":
        delete_current_callback_message(call)
        state = State.get_state(state_id=4)
        name = state["name"] if state and state.get("name") else "Неизвестное государство"
        text = f"Вы выбрали государство: {name}. Подойдите к капитану, он введёт вас в курс дела."
        User.insert_user(user_id=call.from_user.id, state_id=4)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # ++++++++++++++++++++++++++++++++ ВЫБОР КЛАССА ++++++++++++++++++++++++++++++

    elif call.data == "class_selection":
        delete_current_callback_message(call)
        text = "Бла бла бла, ты нам нужен. Как ты предпочитаешь драться в бою?\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "class_selection_1":
        delete_current_callback_message(call)
        text = (
            "Описание класса <Маг>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "class_selection_2":
        delete_current_callback_message(call)
        text = (
            "Описание класса <Рыцарь>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_2()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "class_selection_3":
        delete_current_callback_message(call)
        text = (
            "Описание класса <Лучник>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_3()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "class_selection_4":
        delete_current_callback_message(call)
        text = (
            "Описание класса <Ассасин>.\n\n"
            "Тут должен быть текст про описание класса и маленькая часть лора этого персонажа."
        )
        markup = inline.Plot.introduction_class_description_4()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    # ++++++++++++++++++++++++++++++++ ПОДТВЕРЖДЕНИЕ КЛАССА ++++++++++++++++++++++++++++++

    elif call.data == "select_class_1":
        delete_current_callback_message(call)
        text = "Ты выбрал класс <Маг>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=1)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_class_2":
        delete_current_callback_message(call)
        text = "Ты выбрал класс <Рыцарь>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=2)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_class_3":
        delete_current_callback_message(call)
        text = "Ты выбрал класс <Лучник>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=3)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_class_4":
        delete_current_callback_message(call)
        text = "Ты выбрал класс <Ассасин>."
        User.set_field(user_id=call.from_user.id, field="class_id", value=4)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ################################# КНОПКИ В БЫСТРОЙ ПАНЕЛИ #################################

    elif call.data == "profile_class":
        delete_current_callback_message(call)
        user = User.get_user(user_id=call.from_user.id)
        if user and user.get("class_id"):
            user_class = UserClass.get_class(class_id=user["class_id"])
            class_name = user_class["name"] if user_class and user_class.get("name") else "Неизвестный класс"
            text = f"Тут должно быть описание класса {class_name}"
        else:
            text = "Класс не выбран."
        markup = inline.Profile.profile_class()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "profile_subclass":
        delete_current_callback_message(call)
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
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "profile_skills":
        delete_current_callback_message(call)
        send_and_track_message(chat_id=chat_id, text="В разработке")

    elif call.data in ("profile_class_back", "profile_subclass_back"):
        delete_current_callback_message(call)
        text = User.get_user_text(user_id=call.from_user.id)
        markup = inline.Profile.profile_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "profile_back":
        delete_current_callback_message(call)
        pass

    elif call.data == "profile_delete_confirm":
        delete_current_callback_message(call)
        text = (
            "Ты точно хочешь удалить профиль?\n\n"
            "Это действие удалит твою запись из базы данных."
        )
        markup = inline.Profile.profile_delete_confirm()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "profile_delete_no":
        delete_current_callback_message(call)
        text = User.get_user_text(user_id=call.from_user.id)
        markup = inline.Profile.profile_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "profile_delete_yes":
        delete_current_callback_message(call)
        try:
            User.delete_user(user_id=call.from_user.id)
            send_and_track_message(
                chat_id=chat_id,
                text="Профиль удалён. Чтобы начать заново, нажми /start."
            )
        except Exception as e:
            print("delete_user error:", repr(e))
            send_and_track_message(
                chat_id=chat_id,
                text="Не удалось удалить профиль. Попробуй ещё раз позже."
            )