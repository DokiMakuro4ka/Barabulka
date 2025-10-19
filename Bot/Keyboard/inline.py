from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Plot:

    def introduction_1():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Далее", callback_data="Далее")
        markup.row(button_1)

        return markup


    def introduction_2():
        markup = InlineKeyboardMarkup()

        button_1 = InlineKeyboardButton(text="🔥 Император Огня 🔥", callback_data="🔥 Император Огня 🔥")
        button_2 = InlineKeyboardButton(text="💧 Принцеса Воды 💧", callback_data="💧 Принцеса Воды 💧")
        button_3 = InlineKeyboardButton(text="💨 Царица Ветра 💨", callback_data="💨 Царица Ветра 💨")
        button_4 = InlineKeyboardButton(text="🪨 Царь Земли 🪨", callback_data="🪨 Царь Земли 🪨")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)

        return markup
