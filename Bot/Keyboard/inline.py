from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Plot:

    def introduction_lor():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Далее", callback_data="class_selection")
        markup.row(button_1)
        return markup

    def introduction_class_selection():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="🔥 Император Огня 🔥", callback_data="class_selection_fire")
        button_2 = InlineKeyboardButton(text="💧 Принцеса Воды 💧", callback_data="class_selection_water")
        button_3 = InlineKeyboardButton(text="💨 Царица Ветра 💨", callback_data="class_selection_wind")
        button_4 = InlineKeyboardButton(text="🪨 Царь Земли 🪨", callback_data="class_selection_land")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    def introduction_class_description_fire():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_fire")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_water():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_water")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_wind():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_wind")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_land():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_land")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup
