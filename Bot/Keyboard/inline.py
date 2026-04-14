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
        button_2 = InlineKeyboardButton(text="Северное Молчание", callback_data="state_selection_Northern_Silence")
        button_3 = InlineKeyboardButton(text="Пылающий Предел", callback_data="state_selection_Burning_Limit")
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
    
    ########################## ГОСУДАРСТВА СЕВЕРНОЕ МОЛЧАНИЕ ##########################
    # Северное Молчание
    def introduction_state_description_Northern_Silence():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_Northern_Silence")
        button_2 = InlineKeyboardButton(text="Эпоха Живого Севера", callback_data="The_Era_of_the_Living_North")
        button_3 = InlineKeyboardButton(text="Эпоха Второго Падения Солнца", callback_data="The_Era_of_the_Second_Fall_of_the_Sun")
        button_4 = InlineKeyboardButton(text="Эпоха Статичного Неба", callback_data="The_Era_of_the_Stationary_Sky")
        button_5 = InlineKeyboardButton(text="Эпоха Медленного Похода", callback_data="The_Era_of_the_Slow_Procession")
        button_6 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        markup.row(button_5)
        markup.row(button_6)
        return markup
    
    # кнопки эпохи живого севера
    def introduction_state_Northern_Silence_The_Era_of_the_Living_North():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Культура", callback_data="The_Era_of_the_Living_North_Culture")
        button_2 = InlineKeyboardButton(text="Конфликты", callback_data="The_Era_of_the_Living_North_Conflicts")
        button_3 = InlineKeyboardButton(text="Магия и вера", callback_data="The_Era_of_the_Living_North_Magic_and_Faith")
        button_4 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Northern_Silence")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup
    
    # кнопки эпохи второго падения солнца
    def introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Катастрофа", callback_data="The_Era_of_the_Second_Sun_Fall_Catastrophe")
        button_2 = InlineKeyboardButton(text="Преображение Мириэль", callback_data="The_Era_of_the_Second_Sun_Fall_Miriel_Transformation")
        button_3 = InlineKeyboardButton(text="Реакция мира", callback_data="The_Era_of_the_Second_Sun_Fall_World_Reaction")
        button_4 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Northern_Silence")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup
    
    # кнопки эпохи статичного неба
    def introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Общество и контроль", callback_data="The_Era_of_the_Stationary_Sky_Life_in_Static")
        button_2 = InlineKeyboardButton(text="Маги статики (Арктик-маги)", callback_data="The_Era_of_the_Stationary_Sky_Arctic_Mages")
        button_3 = InlineKeyboardButton(text="Известные фигуры", callback_data="The_Era_of_the_Stationary_Sky_Notable_Figures")
        button_4 = InlineKeyboardButton(text="Внутренние трения", callback_data="The_Era_of_the_Stationary_Sky_Internal_Tensions")
        button_5 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Northern_Silence")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        markup.row(button_5)
        return markup
    
    # кнопки эпохи медленного похода
    def introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Внешняя экспансия", callback_data="The_Era_of_the_Slow_Procession_External_Expansion")
        button_2 = InlineKeyboardButton(text="Идеология похода", callback_data="The_Era_of_the_Slow_Procession_Ideology_of_the_Procession")
        button_3 = InlineKeyboardButton(text="Конфликты с другими силами", callback_data="The_Era_of_the_Slow_Procession_Conflicts_with_Other_Forces")
        button_4 = InlineKeyboardButton(text="Предатели и сомневающиеся", callback_data="The_Era_of_the_Slow_Procession_Traitors_and_Doubters")
        button_5 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Northern_Silence")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        markup.row(button_5)
        return markup

    ########################## ГОСУДАРСТВА Пылающый Предел ##########################
    # Пылающий предел
    def introduction_state_description_Burning_Limit():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Выбрать государство", callback_data="select_state_Burning_Limit")
        button_2 = InlineKeyboardButton(text="Эпоха Пепельных Королевств", callback_data="The_Era_of_the_Ashen_Kingdoms")
        button_3 = InlineKeyboardButton(text="Эпоха Восстания Пламени", callback_data="The_Era_of_the_Fire_Rebellion")
        button_4 = InlineKeyboardButton(text="Эпоха Железного Правления", callback_data="The_Era_of_the_Iron_Rule")
        button_5 = InlineKeyboardButton(text="Эпоха Похода к Долине", callback_data="bl5")
        button_6 = InlineKeyboardButton(text="Назад", callback_data="state_selection")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        markup.row(button_5)
        markup.row(button_6)
        return markup
    
    # кнопки эпохи Пепельных Королевств
    def introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Культура", callback_data="The_Era_of_the_Ashen_Kingdoms_Culture")
        button_2 = InlineKeyboardButton(text="Конфликты", callback_data="The_Era_of_the_Ashen_Kingdoms_Conflicts")
        button_3 = InlineKeyboardButton(text="Магия и воины", callback_data="The_Era_of_the_Ashen_Kingdoms_Magic_and_Warriors")
        button_4 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Burning_Limit")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    # кнопки эпохи Восстания Пламени
    def introduction_state_Burning_The_Era_of_the_Fire_Rebellion():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Возвышение Хомусуби", callback_data="The_Era_of_the_Fire_Rebellion_The_Rise_of_Homusubi")
        button_2 = InlineKeyboardButton(text="Слом старых королевств", callback_data="The_Era_of_the_Fire_Rebellion_The_Fall_of_the_Old_Kingdoms")
        button_3 = InlineKeyboardButton(text="Рождение особой гвардии", callback_data="The_Era_of_the_Fire_Rebellion_The_Birth_of_the_Special_Guard")
        button_4 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Burning_Limit")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    # кнопки эпохи Железного Правления
    def introduction_state_Burning_The_Era_of_the_Iron_Rule():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Общество и контроль", callback_data="The_Era_of_the_Iron_Rule_Society_and_Control")
        button_2 = InlineKeyboardButton(text="Ассасины как сущность Предела", callback_data="The_Era_of_the_Iron_Rule_Assassins_as_a_Pillar_of_the_Limit")
        button_3 = InlineKeyboardButton(text="Известные ассасины", callback_data="The_Era_of_the_Iron_Rule_Famous_Assassins")
        button_4 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Burning_Limit")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
        return markup

    # кнопки эпохи Похода к Долине
    def ISB_The_Era_of_the_Exp_to_the_Valley():
        markup = InlineKeyboardMarkup()
        button_1 = InlineKeyboardButton(text="Стратегическая цель", callback_data="The_Era_of_the_Exp_to_the_Vall_Strat_Obj")
        button_2 = InlineKeyboardButton(text="Роль особой гвардии и ассасинов", callback_data="The_Era_of_the_Exp_to_the_Valley_Spec_Guard_and_Assas_Rol")
        button_3 = InlineKeyboardButton(text="Идеология экспансии", callback_data="The_Era_of_the_Exp_to_the_Valley_Ideol_of_Exp")
        button_4 = InlineKeyboardButton(text="Назад", callback_data="state_selection_Burning_Limit")
        markup.row(button_1)
        markup.row(button_2)
        markup.row(button_3)
        markup.row(button_4)
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
        button_2 = InlineKeyboardButton(text="Назад", callback_data="subclass_selection_2")
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
