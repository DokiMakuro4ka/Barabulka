from bot import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class Plot:
    def introduction_1():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton("Далее")
        markup.row(button_1)

        return markup

    def introduction_2():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton("🔥 Император Огня 🔥")
        button_2 = KeyboardButton("💧 Принцеса Воды 💧")
        button_3 = KeyboardButton("💨 Царица Ветра 💨")
        button_4 = KeyboardButton("🪨 Царь Земли 🪨")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)

        return markup
