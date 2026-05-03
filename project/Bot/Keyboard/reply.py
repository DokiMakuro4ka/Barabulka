from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class Plot:
    @staticmethod
    def introduction_1(has_class=False):
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if has_class:
            markup.add(
                KeyboardButton("📊 Профиль"),
                KeyboardButton("⚔️ Сражаться"),
                KeyboardButton("ℹ️ Помощь")
            )
        else:
            markup.add(
                KeyboardButton("📊 Профиль"),
                KeyboardButton("⚔️ Сражаться"),
                KeyboardButton("📜 Выбрать класс"),
                KeyboardButton("ℹ️ Помощь")
            )
        return markup
