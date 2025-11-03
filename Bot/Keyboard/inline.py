from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Plot:
    def introduction_lor():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Далее", callback_data="state_selection")
        markup.row(button_1)
        return markup


    def introduction_state_selection():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Государство 1", callback_data="state_selection_1")
        button_2 = InlineKeyboardButton(text="Государство 2", callback_data="state_selection_2")
        button_3 = InlineKeyboardButton(text="Государство 3", callback_data="state_selection_3")
        button_4 = InlineKeyboardButton(text="Королевство Дварфов", callback_data="state_selection_4")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    def introduction_state_description_1():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_1")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_state_description_2():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_2")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_state_description_3():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_3")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_state_description_4():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_4")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup


    def introduction_class_selection():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Маг", callback_data="class_selection_1")
        button_2 = InlineKeyboardButton(text="Рыцарь", callback_data="class_selection_2")
        button_3 = InlineKeyboardButton(text="Лучник", callback_data="class_selection_3")
        button_4 = InlineKeyboardButton(text="Ассасин", callback_data="class_selection_4")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    def introduction_class_description_1():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_1")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_2():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_2")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_3():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_3")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_4():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_4")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup


class Profile:
    def profile_1():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Класс", callback_data="profile_class")
        button_2 = InlineKeyboardButton(text="Подкласс", callback_data="profile_subclass")
        button_3 = InlineKeyboardButton(text="Навыки", callback_data="profile_skills")
        button_4 = InlineKeyboardButton(text="Скрыть профиль", callback_data="profile_back")
        markup.row(button_1, button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    def profile_class():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Назад", callback_data="profile_class_back")
        markup.row(button_1)
        return markup

    def profile_subclass():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Назад", callback_data="profile_subclass_back")
        markup.row(button_1)
        return markup 
