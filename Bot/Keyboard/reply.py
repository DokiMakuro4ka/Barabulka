from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class Plot:
    def introduction_1():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton(text="👤 Профиль")
        button_2 = KeyboardButton(text="👨 Капитан")
        markup.row(button_1, button_2)
        return markup
