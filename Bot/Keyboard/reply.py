from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class Interface:
    def interface_1():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton(text="👤 Профиль")
        button_2 = KeyboardButton(text="aaaa")
        markup.row(button_1, button_2)
        return markup
