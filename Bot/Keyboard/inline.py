from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Plot:
    def introduction_lor():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Далее", callback_data="class_selection")
        markup.row(button_1)
        return markup

    def introduction_class_selection():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Маг", callback_data="class_selection_mage")
        button_2 = InlineKeyboardButton(text="Рыцарь", callback_data="class_selection_knight")
        button_3 = InlineKeyboardButton(text="Лучник", callback_data="class_selection_archer")
        button_4 = InlineKeyboardButton(text="Ассасин", callback_data="class_selection_assassin")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    def introduction_class_description_mage():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_mage")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_knight():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_knight")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_archer():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_archer")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="class_selection")
        markup.row(button_1)
        markup.row(button_2)
        return markup

    def introduction_class_description_assassin():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать класс", callback_data="select_class_assassin")
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
