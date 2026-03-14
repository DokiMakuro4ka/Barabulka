import os
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout, SSLError
from telebot.apihelper import ApiTelegramException

from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User

load_dotenv()

START_PHOTO_ID_LOR = os.getenv("START_PHOTO_ID_LOR")
START_PHOTO_ID_AIKATSU = os.getenv("START_PHOTO_ID_AIKATSU")
START_PHOTO_ID_DWARVES = os.getenv("START_PHOTO_ID_DWARVES")

PHOTO_IDS = {
    "lor": START_PHOTO_ID_LOR,
    "aikatsu": START_PHOTO_ID_AIKATSU,
    "dwarves": START_PHOTO_ID_DWARVES,
}

if not PHOTO_IDS["lor"]:
    raise RuntimeError("Переменная START_PHOTO_ID_LOR не найдена в .env")


@bot.message_handler(commands=["start"])
def handler_command_start(message):
    user = User.get_user(message.from_user.id)

    if user is None:
        text = (
            "Тьма окутала Долину Природы, как бездонная ночь. Реки, некогда сиявшие "
            "золотом, застынули в ледяной тишине. Деревья стояли безмолвные, цветы — "
            "опавшие лепестки под тяжестью горя. Ветер приносил лишь крики разрушенных земель."
        )
        markup = inline.Plot.introduction_lor()

        try:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=PHOTO_IDS["lor"],
                caption=text,
                reply_markup=markup,
            )
        except (ApiTelegramException, ConnectionError, Timeout, SSLError, OSError) as e:
            print("send_photo error:", repr(e))
            bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=markup,
            )
    else:
        markup = reply.Plot.introduction_1()
        bot.send_message(
            chat_id=message.chat.id,
            text="Ты уже зарегистрирован",
            reply_markup=markup,
        )