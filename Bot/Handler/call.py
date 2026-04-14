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
STATE_ICE_PHOTO_ID = os.getenv("START_PHOTO_ID_ICE")
KINGDOM_FIRE_PHOTO_ID = os.getenv("START_PHOTO_ID_FIRE")

PHOTO_IDS = {
    "aikatsu": STATE_AIKATSU_PHOTO_ID,
    "dwarves": KINGDOM_DWARVES_PHOTO_ID,
    "ice": STATE_ICE_PHOTO_ID,
    "fire": KINGDOM_FIRE_PHOTO_ID,
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

    # -------------------------------- ГОСУДАРСТВО Северное Молчание -------------------------------

    elif call.data == "state_selection_Northern_Silence":
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
        markup = inline.Plot.introduction_state_description_Northern_Silence()

        photo_id = PHOTO_IDS["ice"]
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

    ## -------------------------------- "Эпоха живого севера" -------------------------------
    elif call.data == "The_Era_of_the_Living_North":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"До Второго Падения Солнца север был обычным, суровым, но живым королевством, где племена следовали ритмам сезонов, а лед и море сосуществовали с дикой природой.\n\n"
                "Люди жили в городах-портах и кочевых поселениях, поклоняясь северным ветрам как духам перемен."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Культура живого севера" --------------------------------
    elif call.data == "The_Era_of_the_Living_North_Culture":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"До статики северяне почитали циклы смены льда и оттепелей, устраивали праздники первой оттепели и последнего снега, считая движение времён священным.\n\n"
                "Музыка представляла собой протяжные хоры и ритуальные барабаны, имитирующие треск льда и шум волн, а сказители передавали истории о живых ветрах, которые могли менять судьбу человека."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Конфликты живого севера" -------------------------------
    elif call.data == "The_Era_of_the_Living_North_Conflicts":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Главными конфликтами были не войны, а споры между племенами и городами за ресурсы: рыбу, меха и безопасные пути через ледяные плато.\n\n"
                "Иногда возникали локальные войны между родами, но они завершались «Ночью Перемирия», когда все кланы собирались у общего костра, чтобы не допустить разрушения общей земли."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Магия и вера живого севера" ----------------------------
    elif call.data == "The_Era_of_the_Living_North_Magic_and_Faith":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Маги этого периода работали с движением — ветром, волнами, снегопадами, усиливая или ослабляя природные процессы, но не вмешиваясь в саму ткань реальности.\n\n"
                "Вера опиралась на идею, что мир жив, а любой застой — знак болезни, поэтому остановка времени считалась древним проклятием, о котором шёпотом говорили в легендах."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ## -------------------------------- "Эпоха второго падения солнца" -------------------------------
    elif call.data == "The_Era_of_the_Second_Fall_of_the_Sun":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Второе Падение Солнца было катастрофой, когда солнце внезапно погрузилось в затмение, и север погрузился в вечную зиму. Это событие стало началом Статики — периода, когда время остановилось, а земля замерзла.\n\n"
                "Северяне были вынуждены адаптироваться к новому миру, где движение стало невозможным, а жизнь превратилась в борьбу за выживание в ледяной пустыне."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Катастрофа второго падения солнца" -------------------------------
    elif call.data == "The_Era_of_the_Second_Sun_Fall_Catastrophe":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Второе Падение Солнца началось с того, что свет над севером стал тускнеть и дробиться, а тени вытянулись и перестали двигаться, словно кто-то задержал дыхание мира.\n\n"
                "Небо застыло между рассветом и закатом, а время словно потекло вниз — в трещины льда и глубины озёр, вызывая искажения восприятия у людей и магов."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Преображение Мириэль" -------------------------------
    elif call.data == "The_Era_of_the_Second_Sun_Fall_Miriel_Transformation":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Королева Мириэль, пытаясь остановить распад реальности, провела запрещённый ритуал соединения сознания с атмосферой и кристаллическим светом северных небес.\n\n"
                "Ритуал разрушил её человеческую природу: теперь она воспринимает мир через структуру материи и потоки статики, став Белой Тишиной, правящей без крика, а через форму и порядок."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Реакция мира" -------------------------------
    elif call.data == "The_Era_of_the_Second_Sun_Fall_World_Reaction":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Часть подданных увидела в Мириэль спасительницу, которая сохранила север от полного исчезновения, закрепив его во времени.\n\n"
                "Другие восприняли её как начало новой тирании, где сама возможность изменяться будет объявлена преступлением, и попытались бежать на юг, теряясь в исковерканном пространстве."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ## -------------------------------- "Эпоха статичного неба" -------------------------------
    elif call.data == "The_Era_of_the_Stationary_Sky":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Эпоха Статичного Неба — это время, когда север погрузился в вечную зиму и застой. Время остановилось, земля замерзла, и жизнь превратилась в борьбу за выживание в ледяной пустыне.\n\n"
                "Северяне были вынуждены адаптироваться к новому миру, где движение стало невозможным, а жизнь превратилась в борьбу за выживание в ледяной пустыне."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Общество и контроль" -------------------------------
    elif call.data == "The_Era_of_the_Stationary_Sky_Life_in_Static":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"В Северном Молчании время измеряется не днями, а степенью неподвижности: чем меньше изменяется район, тем он считается «здоровее» и ближе к идеалу Мириэль.\n\n"
                "Города превращены в геометрически совершенные структуры, где движение строго регламентировано, а любые спонтанные собрания или праздники воспринимаются как симптом хаоса."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Маги статики (Арктик-маги)" -------------------------------
    elif call.data == "The_Era_of_the_Stationary_Sky_Arctic_Mages":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Арктик-маги — это архитекторы покоя, которые переписывают физику пространства, замедляя всё, что нарушает заданный ритм.\n\n"
                "Их главная способность «Кристаллизация Реальности» позволяет остановить фрагмент мира, где скорость движения существ подчиняется ритму их собственного сердца, а не их воле."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Известные фигуры" -------------------------------
    elif call.data == "The_Era_of_the_Stationary_Sky_Notable_Figures":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Мириэль, Белая Тишина, стала не столько правителем, сколько распределённым сознанием, наблюдающим за каждым кристаллом льда и каждым изменением в атмосфере\n\n"
                "Аэллар, Монах Фракталов, создаёт зеркальные структуры, отражающие не только удары, но и намерения, что делает любые мятежи практически невозможными."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ###-------------------------------- "Внутренние трения" -------------------------------
    elif call.data == "The_Era_of_the_Stationary_Sky_Internal_Tensions":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Часть жителей смирилась и даже нашла покой в предсказуемости и статичности, считая её защитой от нового конца света.\n\n"
                "Другая часть ощущает, что вместе с хаосом из мира ушли радость, творчество и любовь, и тайно ищет способы вернуть хотя бы малую долю движения в свою жизнь."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ## -------------------------------- "Эпоха медленного похода" -------------------------------
    elif call.data == "The_Era_of_the_Slow_Procession":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Государство льда начинает медленное наступление на юг, к Долине Природы, стремясь навязать ей закон тишины и остановленного времени.\n\n"
                "Мириэль видит в Долине последний очаг неконтролируемой жизни и верит, что её подчинение позволит человечеству избежать нового распада."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Внешняя экспансия" -------------------------------
    elif call.data == "The_Era_of_the_Slow_Procession_External_Expansion":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Северное Молчание начинает «поход без маршей»: армии движутся медленно, но неуклонно, превращая каждую захваченную территорию в более статичную и управляемую.\n\n"
                "Их цель — Долина Природы, последний регион, где мир живёт собственным ритмом, не подчиняясь ни одному закону статики."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Идеология похода" -------------------------------
    elif call.data == "The_Era_of_the_Slow_Procession_Ideology_of_the_Procession":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Мириэль убеждена, что uncontrolled жизнь, подверженная изменениям, неизбежно придёт к новому Падению, поэтому остановка — единственный настоящий акт милосердия.\n\n"
                "С точки зрения Северного Молчания, заморозить Долину во времени — значит навсегда сохранить её красоту и остановить возможность гибели."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Конфликты с другими силами" -------------------------------
    elif call.data == "The_Era_of_the_Slow_Procession_Conflicts_with_Other_Forces":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Государства Огня, Земли и Айкацу видят в походе Северного Молчания угрозу самому понятию свободы и естественного движения, поэтому пытаются остановить продвижение льда.\n\n"
                "На границах возникают зоны, где статика льда сталкивается с магией ветра, пламенем и живой землёй, создавая искажённые области, где законы мира постоянно переписываются."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Предатели и сомневающиеся" -------------------------------
    elif call.data == "The_Era_of_the_Slow_Procession_Traitors_and_Doubters":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=2)
        text = (
                f"Тарин, Клятвопреступник, перешёл на сторону Мириэль после того, как увидел, как его народ в Долине тонет в хаосе и внутренней борьбе, и поверил в «спасение через остановку».\n\n"
                "В то же время внутри Северного Молчания появляется малое число магов, которые начинают сомневаться, действительно ли вечная статика лучше смертной, но живой жизни."
            )
        markup = inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    # -------------------------------- ГОСУДАРСТВО Пылающий Предел -------------------------------
    elif call.data == "state_selection_Burning_Limit":
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
        markup = inline.Plot.introduction_state_description_Burning_Limit()
        
        photo_id = PHOTO_IDS["fire"]
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

    ## -------------------------------- "Эпоха Пепельных Королевств" -------------------------------
    elif call.data == "The_Era_of_the_Ashen_Kingdoms":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Время, когда на месте Предела существовали разрозненные огненные королевства, сражающиеся друг с другом за ресурсы и власть, пока земля уже дышала жаром, но ещё не была объединена.\n\n"
            "Люди привыкли к боли и суровым условиям, но не имели единой цели, а пламя считали лишь опасной стихией, а не основой своей судьбы."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### ------------------------------- "Культура" -------------------------------
    elif call.data == "The_Era_of_the_Ashen_Kingdoms_Culture":  
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"До возвышения Хомусуби люди Предела жили в небольших королевствах и кланах, где культ огня существовал, но не имел единого богословия или идеологии.\n\n"
            "Праздники были связаны с выживанием: почитали тех, кто пережил засухи, пожары и извержения, а рассказы старейшин были наполнены историями о том, как огонь забирает и даёт жизнь."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### ------------------------------- "Конфликты" -------------------------------
    elif call.data == "The_Era_of_the_Ashen_Kingdoms_Conflicts":  
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Основные войны велись между самими огненными королевствами за владение источниками тепла, металлургическими центрами и безопасными путями через обугленные земли.\n\n"
            "Не было единого врага — каждый клан считал своих соседей главной угрозой, а внешние земли воспринимались лишь как далёкие слухи."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### ------------------------------- "Магия и воины" -------------------------------
    elif call.data == "The_Era_of_the_Ashen_Kingdoms_Magic_and_Warriors":  
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Боевое ремесло развивалось хаотично: одни кланы делали ставку на тяжёлую пехоту, другие — на быстрых налётчиков, которые использовали дым и жар как прикрытие.\n\n"
            "Ассасины как отдельный класс ещё не существовали, но уже были отдельные убийцы, которые использовали огонь как отвлекающий фактор и инструмент для скрытого проникновения."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ## -------------------------------- "Эпоха Восстания Пламени" -------------------------------
    elif call.data == "The_Era_of_the_Fire_Rebellion":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Период, когда Хомусуби поднялся из пепла старых королевств, объединил их силой и страхом и превратил разрозненные земли в Пылающий Предел.\n\n"
            "Огненный Император создал систему железной дисциплины и тайной гвардии, которая устраняла всех противников его власти."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### ------------------------------- "Возвышение Хомусуби" -------------------------------
    elif call.data == "The_Era_of_the_Fire_Rebellion_The_Rise_of_Homusubi":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Хомусуби собрал вокруг себя тех, кто был не удовлетворён вечными междоусобицами, и предложил идею единого Предела, где огонь станет не просто стихией, а законом.\n\n"
            "Он использовал страх как рычаг: демонстративные казни и сожжения врагов показали, что сопротивление приведёт лишь к превращению в пепел, укрепив его власть через ужас и восторг."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Слом старых королевств" -------------------------------
    elif call.data == "The_Era_of_the_Fire_Rebellion_The_Fall_of_the_Old_Kingdoms":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Старые династии были либо уничтожены, либо ассимилированы в новую структуру империи Пылающего Предела, их символы сгорели в огненных ритуалах объединения.\n\n"
            "Города, которые подчинились, получили шанс стать центрами производства оружия и обучения воинов, а непокорные были стерты до камня и пепла."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Рождение особой гвардии" -------------------------------
    elif call.data == "The_Era_of_the_Fire_Rebellion_The_Birth_of_the_Special_Guard":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"В это время Хомусуби создал закрытое братство особой гвардии — безжалостных и бесшумных воинов, обученных действовать там, где армия бессильна.\n\n"
            "Из этого братства позднее выделились ассасины Предела, ставшие личным инструментом Императора для устранения заговорщиков, предателей и внешних врагов."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ## -------------------------------- "Эпоха Железного Правления" -------------------------------
    elif call.data == "The_Era_of_the_Iron_Rule":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Установив контроль, Хомусуби превратил страх подданных в топливо для великого огня, питающего его могущество и военную машину государства.\n\n"
            "Предел стал государством вечного жара и строгого воинского порядка, где каждый гражданин рассматривается как ресурс для поддержания пламени."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Общество и контроль" -------------------------------
    elif call.data == "The_Era_of_the_Iron_Rule_Society_and_Control":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Под властью Хомусуби Пылающий Предел превратился в государство, где дисциплина и страх стали основой каждого дня, а слабость считается преступлением против империи.\n\n"
            "Дети с ранних лет обучаются выносливости, терпению боли и владению оружием, а те, кто не выдерживает, становятся живым примером того, что огонь не терпит хрупкости."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Ассасины как сущность Предела" -------------------------------
    elif call.data == "The_Era_of_the_Iron_Rule_Assassins_as_a_Pillar_of_the_Limit":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Ассасины Пылающего Предела — не просто убийцы, а живые воплощения идеи, что пламя должно прожигать препятствия изнутри, а не только снаружи.\n\n"
            "Их стиль боя сочетает скорость, выносливость и абсолютный контроль над телом, позволяя действовать в самом центре битвы, а не только из тени."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Известные ассасины" -------------------------------
    elif call.data == "The_Era_of_the_Iron_Rule_Famous_Assassins":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Момоти — хладнокровный охотник с кусаригамой, удерживающий врагов в смертельной дистанции, словно пламя держит жертву на грани обугливания.\n\n"
            "Кенджи владеет парой кинжалов, так быстро рассекающих воздух, что тот словно вспыхивает от трения, превращая каждую атаку в вспышку ярости.\n\n"
            "Сакато с кастетами верит, что убийца обязан чувствовать жар жизни цели, превращая ближний бой в бурю ударов и искр.\n\n"
            "Джейкоб, чужеземец с тяжёлой катаной, стал символом того, что Предел принимает тех, кто готов сгореть и возродиться в огне дисциплины и безмолвной ярости."
        )
        markup = inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ## -------------------------------- "Эпоха Похода к Долине" -------------------------------
    elif call.data == "bl5":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Современный период, когда Пылающий Предел направляет свою силу наружу, стремясь захватить Долину Природы как ключ к ресурсам и окончательному утверждению власти огня над миром.\n\n"
            "Ассасины и армии Предела действуют скрытно и открыто, чтобы превратить Долину в священный символ победы пламени."
        )
        markup = inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)
    
    ### -------------------------------- "Стратегическая цель" -------------------------------
    elif call.data == "The_Era_of_the_Exp_to_the_Vall_Strat_Obj":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Официальная и скрытая цель Пылающего Предела — захват и подчинение Долины Природы, плодородного оазиса, который может обеспечить империи ресурсы и контроль над ключевыми землями.\n\n"
            "Долина рассматривается не только как источник пищи и удобства, но и как священное место, где власть огня должна быть утверждена окончательно."
        )
        markup = inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Роль особой гвардии и ассасинов" -------------------------------
    elif call.data == "The_Era_of_the_Exp_to_the_Valley_Spec_Guard_and_Assas_Rol":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"Особая гвардия и ассасины Предела отправляются в Долину и соседние регионы с задачами устранения лидеров сопротивления, подрыва доверия между фракциями и создания ощущения неизбежности победы огня.\n\n"
            "Они действуют как тень Императора: никто не знает, где они появятся, но каждый понимает, что любой, кто встанет на пути Хомусуби, может исчезнуть в пламени без следа."
        )
        markup = inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    ### -------------------------------- "Идеология экспансии" -------------------------------
    elif call.data == "The_Era_of_the_Exp_to_the_Valley_Ideol_of_Exp":
        delete_current_callback_message(call)
        state = UserState.get_state(state_id=3)
        text = (
            f"С точки зрения Предела, мир должен либо сгореть, либо преклониться перед огнём: тот, кто не выдерживает жара, не достоин выживания.\n\n"
            "Пылающий Предел убеждён, что только тот, кто живёт на грани боли и смерти, имеет право диктовать условия остальному миру."
        )
        markup = inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley()
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

    elif call.data == "select_state_Northern_Silence":
        delete_current_callback_message(call)
        text = "Вы выбрали государство Северное Молчание."
        User.insert_user(user_id=call.from_user.id, state_id=2)
        markup = reply.Plot.introduction_1()
        send_and_track_message(chat_id=chat_id, text=text, reply_markup=markup)

    elif call.data == "select_state_Burning_Limit":
        delete_current_callback_message(call)
        text = "Вы выбрали государство Пылающий предел."
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