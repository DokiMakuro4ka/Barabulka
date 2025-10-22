from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class Plot:

    def introduction_lor():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton("Далее")
        markup.row(button_1)
        return markup


class Location:
    pass
