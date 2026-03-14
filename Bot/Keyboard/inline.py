from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Plot:
    def introduction_lor():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Далее", callback_data="state_selection")
        markup.row(button_1)
        return markup


    def introduction_state_selection():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Айкацу", callback_data="state_selection_aikatsu")
        button_2 = InlineKeyboardButton(text="Государство 2", callback_data="state_selection_2")
        button_3 = InlineKeyboardButton(text="Государство 3", callback_data="state_selection_3")
        button_4 = InlineKeyboardButton(text="Королевство Дварфов", callback_data="state_selection_4")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    ########################## ГОСУДАРСТВА АЙКАТСУ ##########################
    # Кнопки государства айкатсу
    def introduction_state_aikatsu():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_aikatsu")
        button_2 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        button_3 = InlineKeyboardButton(text="Эпоха Тумана (до объединения)", callback_data="The_Age_of_Fog")
        button_4 = InlineKeyboardButton(text="Эпоха Объединения (основание Айкацу)", callback_data="The_Era_of_Unification")
        button_5 = InlineKeyboardButton(text="Эпоха Парящих Врат (нынешнее время)", callback_data="The_Age_of_Floating_Gates")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        markup.row(button_5)
        return markup
    
    # кнопки эпохи тумана
    def introduction_state_aikatsu_The_Age_of_Fog():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Назад", callback_data="state_selection_aikatsu")
        button_2 = InlineKeyboardButton(text="⚔️ Конфликты", callback_data="conflicts_The_Age_of_Fog")
        button_3 = InlineKeyboardButton(text="🌫️ Культура", callback_data="Culture_The_Age_of_Fog")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        return markup
    
    # кнопки эпохи объединения
    def introduction_state_aikatsu_The_Era_of_Unification():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Назад", callback_data="state_selection_aikatsu")
        button_2 = InlineKeyboardButton(text="📜 Кодекс Воздушного Пути", callback_data="The_Era_of_Unification_The_Code_of_the_Air_Path")
        button_3 = InlineKeyboardButton(text="🏛️ Небесный Додзё", callback_data="The_Era_of_Unification_The_Celestial_Dojo")
        button_4 = InlineKeyboardButton(text="🤝 Последствия", callback_data="The_Era_of_Unification_The_Consequences")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup
    
    # кнопки эпохи парящих врат
    def introduction_state_aikatsu_The_Age_of_Floating_Gates():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Назад", callback_data="state_selection_aikatsu")
        button_2 = InlineKeyboardButton(text="⚠️ Внешние угрозы", callback_data="The_Age_of_Floating_Gates_External_threats")
        button_3 = InlineKeyboardButton(text="💥 Внутренний конфликт", callback_data="The_Age_of_Floating_Gates_Internal_conflict")
        button_4 = InlineKeyboardButton(text="🧩 Политическая напряжённость", callback_data="The_Age_of_Floating_Gates_Political_tension")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
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
        button_4 = InlineKeyboardButton(text="Удалить профиль", callback_data="profile_delete_confirm")
        button_5 = InlineKeyboardButton(text="Скрыть профиль", callback_data="profile_back")

        markup.row(button_1, button_2)
        markup.row(button_3)
        markup.row(button_4)
        markup.row(button_5)
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

    def profile_delete_confirm():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Да, удалить", callback_data="profile_delete_yes")
        button_2 = InlineKeyboardButton(text="Нет", callback_data="profile_delete_no")
        markup.row(button_1, button_2)
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
