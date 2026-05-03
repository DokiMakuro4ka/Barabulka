import os
import random
import psycopg2
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
from requests.exceptions import ConnectionError, Timeout, SSLError

from TG_bot.config.settings import Config
from TG_bot.DB.centre import (
    User, UserClass, UserSubclass, State, Epoch, EpochDetail, Monster, BattleLog
)
from TG_bot.Bot.Keyboard import reply
from TG_bot.Bot.Keyboard import inline

bot = TeleBot(Config.BOT_TOKEN)
LAST_BOT_MESSAGES = {}
ACTIVE_BATTLES = {}

PHOTO_IDS = {
    "aikatsu": Config.STATE_AIKATSU_PHOTO_ID,
    "dwarves": Config.STATE_DWARVES_PHOTO_ID,
    "ice": Config.STATE_ICE_PHOTO_ID,
    "fire": Config.STATE_FIRE_PHOTO_ID,
    "lor": Config.LOR_ID,
}

def user_has_class(user_id):
    user = User.get_user(user_id)
    if user:
        return user[15] not in (None, 0)
    return False

def delete_tracked_message(chat_id):
    mid = LAST_BOT_MESSAGES.get(chat_id)
    if mid:
        try:
            bot.delete_message(chat_id, mid)
        except:
            pass
        LAST_BOT_MESSAGES.pop(chat_id, None)

def delete_current_callback_message(call):
    chat_id = call.message.chat.id
    mid = call.message.id
    try:
        bot.delete_message(chat_id, mid)
    except:
        pass
    if LAST_BOT_MESSAGES.get(chat_id) == mid:
        LAST_BOT_MESSAGES.pop(chat_id, None)

def send_and_track_message(chat_id, text, reply_markup=None):
    delete_tracked_message(chat_id)
    msg = bot.send_message(chat_id, text, reply_markup=reply_markup)
    LAST_BOT_MESSAGES[chat_id] = msg.message_id
    return msg

def send_and_track_photo(chat_id, photo_id, caption, reply_markup=None, fallback_text=None):
    delete_tracked_message(chat_id)
    try:
        msg = bot.send_photo(chat_id, photo_id, caption=caption, reply_markup=reply_markup)
        LAST_BOT_MESSAGES[chat_id] = msg.message_id
        return msg
    except:
        msg = bot.send_message(chat_id, fallback_text or caption, reply_markup=reply_markup)
        LAST_BOT_MESSAGES[chat_id] = msg.message_id
        return msg

@bot.message_handler(commands=['start'])
def cmd_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if User.get_user(user_id):
        has_class = user_has_class(user_id)
        send_and_track_message(chat_id, "С возвращением! Используй кнопки.", reply.Plot.introduction_1(has_class))
    else:
        lore_text = (
            "🌍 *Добро пожаловать в мир четырёх государств!* 🌍\n\n"
            "С незапамятных времён эти земли хранили гармонию,\n"
            "но теперь великие державы вступили в борьбу за власть.\n\n"
            "✨ *Айкацу* – воздушная магия и дисциплина.\n"
            "❄️ *Северное Молчание* – ледяная статика и время.\n"
            "🔥 *Пылающий Предел* – огонь и железная дисциплина.\n"
            "⛏️ *Дварфы* – горные короли и крепкие тела.\n\n"
            "Ты – новый искатель приключений. Твой путь начинается здесь.\n"
            "Сначала выбери государство, которому будешь служить."
        )
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("⚔️ Выбрать государство", callback_data="state_selection"))
        lore_photo = PHOTO_IDS.get("lor")
        if lore_photo:
            send_and_track_photo(chat_id, lore_photo, lore_text, reply_markup=markup, fallback_text=lore_text)
        else:
            send_and_track_message(chat_id, lore_text, reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"`{file_id}`", parse_mode="Markdown")

@bot.message_handler(commands=['menu'])
def cmd_menu(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    has_class = user_has_class(user_id)
    send_and_track_message(chat_id, "Главное меню:", reply.Plot.introduction_1(has_class))

@bot.message_handler(func=lambda m: m.text == "📊 Профиль")
def profile_handler(message):
    text = User.get_user_text(message.from_user.id)
    send_and_track_message(message.chat.id, text, inline.Plot.profile_1())

@bot.message_handler(func=lambda m: m.text == "📜 Выбрать класс")
def choose_class_handler(message):
    user_id = message.from_user.id
    user = User.get_user(user_id)
    if user and user[15]:  # class_id не 0
        send_and_track_message(message.chat.id, "Твой класс уже выбран! Чтобы сменить класс, нужно удалить профиль и начать заново.", reply.Plot.introduction_1(True))
    else:
        send_and_track_message(message.chat.id, "Выбери класс:", inline.Plot.introduction_class_selection())

@bot.message_handler(func=lambda m: m.text == "⚔️ Сражаться")
def fight_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_data = User.get_user(user_id)
    if not user_data:
        has_class = user_has_class(user_id)
        send_and_track_message(chat_id, "Сначала /start", reply.Plot.introduction_1(has_class))
        return
    with psycopg2.connect(Config.db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT location_id FROM "Users" WHERE telegram_id = %s', (user_id,))
            row = cur.fetchone()
            loc_id = row[0] if row else 1
    monster = Monster.get_random_monster_by_location(loc_id)
    if not monster:
        has_class = user_has_class(user_id)
        send_and_track_message(chat_id, "Нет монстров", reply.Plot.introduction_1(has_class))
        return
    mid, name, lvl, hp, dmg, defence, exp_r, coin_r, _, _ = monster
    ACTIVE_BATTLES[user_id] = {
        "monster": {"id": mid, "name": name, "level": lvl, "hp": hp, "max_hp": hp, "damage": dmg, "defence": defence, "exp_reward": exp_r, "coin_reward": coin_r},
        "player_hp": user_data[7] if isinstance(user_data, tuple) else 100,
        "monster_current_hp": hp
    }
    text = f"⚔️ {name} (ур. {lvl}) ⚔️\n❤️ {hp} HP\nТвоё HP: {ACTIVE_BATTLES[user_id]['player_hp']}"
    send_and_track_message(chat_id, text, inline.Plot.battle_keyboard())

@bot.message_handler(func=lambda m: m.text == "ℹ️ Помощь")
def help_handler(message):
    send_and_track_message(message.chat.id, "/start - начать\n/menu - меню")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    data = call.data
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    # ----- ВЫБОР ГОСУДАРСТВА -----
    if data == "state_selection":
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "Выберите государство:", inline.Plot.introduction_state_selection())
    elif data == "state_selection_aikatsu":
        delete_current_callback_message(call)
        state = State.get_state_by_name("Айкацу")
        desc = state[2] if state else "Описание Айкацу"
        photo = PHOTO_IDS.get("aikatsu")
        if photo:
            send_and_track_photo(chat_id, photo, desc, inline.Plot.introduction_state_aikatsu(), fallback_text=desc)
        else:
            send_and_track_message(chat_id, desc, inline.Plot.introduction_state_aikatsu())
    elif data == "state_selection_Northern_Silence":
        delete_current_callback_message(call)
        state = State.get_state_by_name("Северное Молчание")
        desc = state[2] if state else "Описание Северного Молчания"
        photo = PHOTO_IDS.get("ice")
        if photo:
            send_and_track_photo(chat_id, photo, desc, inline.Plot.introduction_state_description_Northern_Silence(), fallback_text=desc)
        else:
            send_and_track_message(chat_id, desc, inline.Plot.introduction_state_description_Northern_Silence())
    elif data == "state_selection_Burning_Limit":
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "Описание Пылающего Предела (добавьте фото)", inline.Plot.introduction_state_description_Burning_Limit())
    elif data == "state_selection_4":
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "Описание Дварфов", inline.Plot.introduction_state_description_4())

    # ----- ПОДТВЕРЖДЕНИЕ ВЫБОРА ГОСУДАРСТВА (создание пользователя) -----
    elif data == "select_state_aikatsu":
        delete_current_callback_message(call)
        User.insert_user(telegram_id=user_id, state_id=1)
        send_and_track_message(chat_id, "Ты выбрал государство Айкацу. Теперь выбери класс.", inline.Plot.introduction_class_selection())
    elif data == "select_state_Northern_Silence":
        delete_current_callback_message(call)
        User.insert_user(telegram_id=user_id, state_id=2)
        send_and_track_message(chat_id, "Ты выбрал государство Северное Молчание. Теперь выбери класс.", inline.Plot.introduction_class_selection())
    elif data == "select_state_Burning_Limit":
        delete_current_callback_message(call)
        User.insert_user(telegram_id=user_id, state_id=3)
        send_and_track_message(chat_id, "Ты выбрал государство Пылающий Предел. Теперь выбери класс.", inline.Plot.introduction_class_selection())
    elif data == "select_state_4":
        delete_current_callback_message(call)
        User.insert_user(telegram_id=user_id, state_id=4)
        send_and_track_message(chat_id, "Ты выбрал государство Дварфов. Теперь выбери класс.", inline.Plot.introduction_class_selection())

    # ----- ЭПОХИ АЙКАЦУ -----
    elif data == "The_Age_of_Fog":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Fog())

    elif data == "conflicts_The_Age_of_Fog":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Конфликты")
            text = det[3] if det else "Конфликты не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Fog())

    elif data == "Culture_The_Age_of_Fog":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Тумана")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Культура")
            text = det[3] if det else "Культура не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Fog())

    elif data == "The_Era_of_Unification":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Объединения")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Era_of_Unification())

    elif data == "The_Era_of_Unification_The_Code_of_the_Air_Path":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Объединения")
        if epoch:
            # Здесь категория "Кодекс Воздуха" – должна быть в EpochDetails
            det = EpochDetail.get_detail_by_category(epoch[0], "Кодекс Воздуха")
            text = det[3] if det else "Кодекс не описан."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Era_of_Unification())

    elif data == "The_Era_of_Unification_The_Celestial_Dojo":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Объединения")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Небесный Додзё")
            text = det[3] if det else "Описание Небесного Додзё не найдено."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Era_of_Unification())

    elif data == "The_Era_of_Unification_The_Consequences":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Объединения")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Последствия")
            text = det[3] if det else "Последствия не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Era_of_Unification())

    elif data == "The_Age_of_Floating_Gates":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Парящих Врат")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates())

    elif data == "The_Age_of_Floating_Gates_External_threats":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Парящих Врат")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Внешние угрозы")
            text = det[3] if det else "Внешние угрозы не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates())

    elif data == "The_Age_of_Floating_Gates_Internal_conflict":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Парящих Врат")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Внутренний конфликт")
            text = det[3] if det else "Внутренний конфликт не описан."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates())

    elif data == "The_Age_of_Floating_Gates_Political_tension":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Парящих Врат")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Политическое напряжение")
            text = det[3] if det else "Политическое напряжение не описано."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_aikatsu_The_Age_of_Floating_Gates())

    # ----- ЭПОХИ СЕВЕРНОГО МОЛЧАНИЯ -----
    elif data == "The_Era_of_the_Living_North":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Живого Севера")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North())

    elif data == "The_Era_of_the_Living_North_Culture":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Живого Севера")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Культура")
            text = det[3] if det else "Культура не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North())

    elif data == "The_Era_of_the_Living_North_Conflicts":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Живого Севера")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Конфликты")
            text = det[3] if det else "Конфликты не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North())

    elif data == "The_Era_of_the_Living_North_Magic_and_Faith":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Живого Севера")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Магия и вера")
            text = det[3] if det else "Магия и вера не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Living_North())

    elif data == "The_Era_of_the_Second_Fall_of_the_Sun":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Второго Падения Солнца")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall())

    elif data == "The_Era_of_the_Second_Sun_Fall_Catastrophe":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Второго Падения Солнца")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Катастрофа")
            text = det[3] if det else "Катастрофа не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall())

    elif data == "The_Era_of_the_Second_Sun_Fall_Miriel_Transformation":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Второго Падения Солнца")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Преображение Мириэль")
            text = det[3] if det else "Преображение не описано."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall())

    elif data == "The_Era_of_the_Second_Sun_Fall_World_Reaction":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Второго Падения Солнца")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Реакция мира")
            text = det[3] if det else "Реакция не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall())

    elif data == "The_Era_of_the_Stationary_Sky":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Статичного Неба")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky())

    elif data == "The_Era_of_the_Stationary_Sky_Life_in_Static":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Статичного Неба")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Жизнь в статике")
            text = det[3] if det else "Жизнь в статике не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky())

    elif data == "The_Era_of_the_Stationary_Sky_Arctic_Mages":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Статичного Неба")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Арктик-маги")
            text = det[3] if det else "Арктик-маги не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky())

    elif data == "The_Era_of_the_Stationary_Sky_Notable_Figures":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Статичного Неба")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Известные фигуры")
            text = det[3] if det else "Известные фигуры не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky())

    elif data == "The_Era_of_the_Stationary_Sky_Internal_Tensions":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Статичного Неба")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Внутренние трения")
            text = det[3] if det else "Внутренние трения не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky())

    elif data == "The_Era_of_the_Slow_Procession":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Медленного Похода")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession())

    elif data == "The_Era_of_the_Slow_Procession_External_Expansion":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Медленного Похода")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Внешняя экспансия")
            text = det[3] if det else "Внешняя экспансия не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession())

    elif data == "The_Era_of_the_Slow_Procession_Ideology_of_the_Procession":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Медленного Похода")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Идеология похода")
            text = det[3] if det else "Идеология не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession())

    elif data == "The_Era_of_the_Slow_Procession_Conflicts_with_Other_Forces":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Медленного Похода")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Конфликты с другими силами")
            text = det[3] if det else "Конфликты не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession())

    elif data == "The_Era_of_the_Slow_Procession_Traitors_and_Doubters":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Медленного Похода")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Предатели и сомневающиеся")
            text = det[3] if det else "Предатели не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession())

    # ----- ЭПОХИ ПЫЛАЮЩЕГО ПРЕДЕЛА -----
    elif data == "The_Era_of_the_Ashen_Kingdoms":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Пепельных Королевств")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms())

    elif data == "The_Era_of_the_Ashen_Kingdoms_Culture":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Пепельных Королевств")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Культура")
            text = det[3] if det else "Культура не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms())

    elif data == "The_Era_of_the_Ashen_Kingdoms_Conflicts":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Пепельных Королевств")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Конфликты")
            text = det[3] if det else "Конфликты не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms())

    elif data == "The_Era_of_the_Ashen_Kingdoms_Magic_and_Warriors":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Пепельных Королевств")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Магия и воины")
            text = det[3] if det else "Магия и воины не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms())

    elif data == "The_Era_of_the_Fire_Rebellion":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Восстания Пламени")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion())

    elif data == "The_Era_of_the_Fire_Rebellion_The_Rise_of_Homusubi":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Восстания Пламени")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Возвышение Хомусуби")
            text = det[3] if det else "Возвышение не описано."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion())

    elif data == "The_Era_of_the_Fire_Rebellion_The_Fall_of_the_Old_Kingdoms":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Восстания Пламени")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Слом старых королевств")
            text = det[3] if det else "Слом старых королевств не описан."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion())

    elif data == "The_Era_of_the_Fire_Rebellion_The_Birth_of_the_Special_Guard":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Восстания Пламени")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Рождение особой гвардии")
            text = det[3] if det else "Рождение особой гвардии не описано."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Fire_Rebellion())

    elif data == "The_Era_of_the_Iron_Rule":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Железного Правления")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule())

    elif data == "The_Era_of_the_Iron_Rule_Society_and_Control":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Железного Правления")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Общество и контроль")
            text = det[3] if det else "Общество и контроль не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule())

    elif data == "The_Era_of_the_Iron_Rule_Assassins_as_a_Pillar_of_the_Limit":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Железного Правления")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Ассасины как опора Предела")
            text = det[3] if det else "Ассасины как опора Предела не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule())

    elif data == "The_Era_of_the_Iron_Rule_Famous_Assassins":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Железного Правления")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Известные ассасины")
            text = det[3] if det else "Известные ассасины не описаны."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.introduction_state_Burning_The_Era_of_the_Iron_Rule())

    elif data == "bl5":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Похода к Долине")
        text = epoch[3] if epoch else "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley())

    elif data == "The_Era_of_the_Exp_to_the_Vall_Strat_Obj":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Похода к Долине")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Стратегическая цель")
            text = det[3] if det else "Стратегическая цель не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley())

    elif data == "The_Era_of_the_Exp_to_the_Valley_Spec_Guard_and_Assas_Rol":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Похода к Долине")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Роль особой гвардии и ассасинов")
            text = det[3] if det else "Роль особой гвардии и ассасинов не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley())

    elif data == "The_Era_of_the_Exp_to_the_Valley_Ideol_of_Exp":
        delete_current_callback_message(call)
        epoch = Epoch.get_epoch_by_name("Эпоха Похода к Долине")
        if epoch:
            det = EpochDetail.get_detail_by_category(epoch[0], "Идеология экспансии")
            text = det[3] if det else "Идеология экспансии не описана."
        else:
            text = "Эпоха не найдена."
        send_and_track_message(chat_id, text, inline.Plot.ISB_The_Era_of_the_Exp_to_the_Valley())

    # ----- КЛАССЫ -----
    elif data == "class_selection":
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "Выбери класс:", inline.Plot.introduction_class_selection())
    elif data.startswith("class_selection_"):
        class_id = data.split("_")[-1]
        descs = {"1": "Маг – стихии, дальний бой", "2": "Рыцарь – танк, защита", "3": "Лучник – криты, дальний", "4": "Ассасин – скрытность, взрывной урон"}
        markup = getattr(inline.Plot, f"introduction_class_description_{class_id}")()
        send_and_track_message(chat_id, descs.get(class_id, "Описание"), markup)
    elif data.startswith("select_class_"):
        class_id = int(data.split("_")[-1])
        print(f"DEBUG: Выбран класс {class_id} для пользователя {user_id}")
        User.set_field(user_id, "class_id", class_id)
        delete_current_callback_message(call)
        has_class = user_has_class(user_id)
        send_and_track_message(chat_id, f"Класс выбран!", reply.Plot.introduction_1(has_class))

    # ----- ПРОФИЛЬ -----
    elif data == "profile_skills":
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "⚡ Навыки в разработке", reply_markup=inline.Plot.profile_1())

    elif data == "profile_delete_confirm":
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "🗑️ Точно удалить профиль? Восстановить будет нельзя.", inline.Plot.profile_delete_confirm())

    elif data == "profile_delete_no":
        delete_current_callback_message(call)
        text = User.get_user_text(user_id)
        send_and_track_message(chat_id, text, inline.Plot.profile_1())

    elif data == "profile_delete_yes":
        delete_current_callback_message(call)
        User.delete_user(user_id)
        has_class = False
        send_and_track_message(chat_id, "Профиль удалён. Напиши /start", reply.Plot.introduction_1(has_class))

    # ----- БОЙ -----
    elif data.startswith("battle_"):
        action = data.split("_")[1]
        battle = ACTIVE_BATTLES.get(user_id)
        if not battle:
            send_and_track_message(chat_id, "Бой не активен")
            return

        monster = battle["monster"]
        player_hp = battle["player_hp"]
        monster_hp = battle["monster_current_hp"]
        turn = battle.get("turn", 1)
        battle_log = battle.get("log", [])

        with psycopg2.connect(Config.db_dsn()) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT damage, defence, max_hp FROM "Users" WHERE telegram_id = %s', (user_id,))
                row = cur.fetchone()
                p_dmg, p_def, p_max_hp = row if row else (15, 5, 100)

        action_desc = ""
        monster_desc = ""
        player_action_log = ""
        monster_action_log = ""

        # ---- Действие игрока ----
        if action == "attack":
            dmg = max(1, p_dmg - monster["defence"] + random.randint(-3, 5))
            monster_hp -= dmg
            action_desc = f"наносишь {dmg} урона!"
            player_action_log = f"⚔️ Ты атакуешь → -{dmg} HP у {monster['name']}"
        elif action == "defend":
            action_desc = "защищаешься"
            player_action_log = f"🛡️ Ты защищаешься (следующий урон монстра снижен)"
        elif action == "flee":
            if random.random() < 0.5:
                # побег успешен
                full_log = "\n".join(battle_log + [f"{turn}. 🏃 Ты сбежал с поля боя!"])
                del ACTIVE_BATTLES[user_id]
                user_data = User.get_user(user_id)
                has_class = bool(user_data[15]) if user_data else False
                send_and_track_message(chat_id, f"Ты сбежал!\n\n{full_log}", reply.Plot.introduction_1(has_class))
                return
            else:
                action_desc = "пытаешься убежать, но не удаётся!"
                player_action_log = f"🏃 Ты попытался убежать, но не смог"
        else:
            return

        # ---- Ход монстра (если жив) ----
        if monster_hp > 0:
            dmg_mod = 0.5 if action == "defend" else 1.0
            m_dmg = max(1, int((monster["damage"] - p_def + random.randint(-2, 3)) * dmg_mod))
            player_hp -= m_dmg
            monster_desc = f"наносит {m_dmg} урона!"
            monster_action_log = f"💥 {monster['name']} атакует → -{m_dmg} HP у тебя"
        else:
            monster_desc = "повержен!"
            monster_action_log = f"🏆 {monster['name']} повержен!"

        # ---- Добавляем строки лога ----
        if player_action_log:
            battle_log.append(f"{turn}. {player_action_log}")
        if monster_action_log and monster_hp > 0:
            battle_log.append(f"{turn}. {monster_action_log}")
        elif monster_hp <= 0:
            battle_log.append(f"{turn}. {monster_action_log}")

        # ---- Проверка смерти игрока ----
        if player_hp <= 0:
            new_hp = p_max_hp // 2
            with psycopg2.connect(Config.db_dsn()) as conn:
                with conn.cursor() as cur:
                    cur.execute('UPDATE "Users" SET hp=%s, current_hp=%s WHERE telegram_id=%s', (new_hp, new_hp, user_id))
                    conn.commit()
            full_log = "\n".join(battle_log + [f"{turn}. 💀 Ты погиб в бою!"])
            del ACTIVE_BATTLES[user_id]
            user_data = User.get_user(user_id)
            has_class = bool(user_data[15]) if user_data else False
            send_and_track_message(chat_id, f"💀 Ты погиб... Воскрес с половиной HP.\n\n{full_log}", reply.Plot.introduction_1(has_class))
            return

        # ---- Проверка победы ----
        if monster_hp <= 0:
            exp_gain = monster["exp_reward"]
            coin_gain = monster["coin_reward"]
            with psycopg2.connect(Config.db_dsn()) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT experience_now, lvl, star_coin FROM "Users" WHERE telegram_id=%s', (user_id,))
                    row = cur.fetchone()
                    if row:
                        exp_now, lvl, coins = row
                        new_exp = exp_now + exp_gain
                        new_lvl = lvl
                        if new_exp >= 100:
                            new_lvl += 1
                            new_exp -= 100
                            cur.execute('UPDATE "Users" SET experience_now=%s, lvl=%s, max_hp=max_hp+10, hp=max_hp, damage=damage+2, defence=defence+1, star_coin=star_coin+%s WHERE telegram_id=%s',
                                        (new_exp, new_lvl, coin_gain, user_id))
                        else:
                            cur.execute('UPDATE "Users" SET experience_now=%s, star_coin=star_coin+%s WHERE telegram_id=%s', (new_exp, coin_gain, user_id))
                        conn.commit()
            BattleLog.save_battle(user_id, monster["id"], "win", exp_gain, coin_gain)
            full_log = "\n".join(battle_log)
            del ACTIVE_BATTLES[user_id]
            user_data = User.get_user(user_id)
            has_class = bool(user_data[15]) if user_data else False
            send_and_track_message(chat_id, f"🏆 Победа!\n\n{full_log}\n\n+{exp_gain} опыта, +{coin_gain} монет", reply.Plot.introduction_1(has_class))
            return

        # ---- Обновляем состояние боя ----
        battle["player_hp"] = player_hp
        battle["monster_current_hp"] = monster_hp
        battle["turn"] = turn + 1
        battle["log"] = battle_log
        ACTIVE_BATTLES[user_id] = battle

        # Обновляем HP игрока в БД
        with psycopg2.connect(Config.db_dsn()) as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE "Users" SET hp=%s, current_hp=%s WHERE telegram_id=%s', (player_hp, player_hp, user_id))
                conn.commit()

        # Берём последние 5 строк лога для краткого отображения
        recent_log = battle_log[-5:]
        log_text = "\n".join(recent_log)
        text = (f"⚔️ Бой с {monster['name']} ⚔️\n"
                f"{log_text}\n\n"
                f"❤️ Твоё HP: {player_hp}\n"
                f"❤️ HP монстра: {monster_hp}/{monster['max_hp']}\n\n"
                f"Что дальше?")
        send_and_track_message(chat_id, text, inline.Plot.battle_keyboard())

    elif data == "battle_log":
        battle = ACTIVE_BATTLES.get(user_id)
        if battle and battle.get("log"):
            full_log = "\n".join(battle["log"])
            send_and_track_message(chat_id, f"📜 История боя:\n{full_log}", reply_markup=inline.Plot.battle_keyboard())
        else:
            send_and_track_message(chat_id, "Лог пуст.", reply_markup=inline.Plot.battle_keyboard())

    elif data == "main_menu":
        delete_current_callback_message(call)
        has_class = user_has_class(user_id)
        send_and_track_message(chat_id, "Главное меню:", reply.Plot.introduction_1(has_class))

    else:
        delete_current_callback_message(call)
        send_and_track_message(chat_id, "Функция в разработке")

def start_bot():
    bot.infinity_polling()