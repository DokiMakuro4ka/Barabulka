from requests.exceptions import ConnectionError, Timeout, SSLError
from telebot.apihelper import ApiTelegramException

from Bot.bot import bot

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
    try:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    except Exception as e:
        print("delete_current_callback_message error:", repr(e))


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
