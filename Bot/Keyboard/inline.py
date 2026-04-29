from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Plot:

    @staticmethod
    def introduction_state_selection():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🏯 Айкацу", callback_data="state_selection_aikatsu"),
            InlineKeyboardButton("❄️ Северное Молчание", callback_data="state_selection_Northern_Silence"),
            InlineKeyboardButton("🔥 Пылающий Предел", callback_data="state_selection_Burning_Limit"),
            InlineKeyboardButton("⛏️ Дварфы", callback_data="state_selection_4")
        )
        return markup

    @staticmethod
    def introduction_state_aikatsu():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📖 Эпоха Тумана", callback_data="The_Age_of_Fog"),
            InlineKeyboardButton("📖 Эпоха Объединения", callback_data="The_Era_of_Unification"),
            InlineKeyboardButton("📖 Эпоха Парящих Врат", callback_data="The_Age_of_Floating_Gates"),
            InlineKeyboardButton("✅ Выбрать Айкацу", callback_data="select_state_aikatsu"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection")
        )
        return markup

    @staticmethod
    def introduction_state_aikatsu_The_Age_of_Fog():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⚔️ Конфликты", callback_data="conflicts_The_Age_of_Fog"),
            InlineKeyboardButton("🎭 Культура", callback_data="Culture_The_Age_of_Fog"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_aikatsu")
        )
        return markup

    @staticmethod
    def introduction_state_aikatsu_The_Era_of_Unification():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📜 Кодекс Пути Ветра", callback_data="The_Era_of_Unification_The_Code_of_the_Air_Path"),
            InlineKeyboardButton("🏛️ Небесный Додзё", callback_data="The_Era_of_Unification_The_Celestial_Dojo"),
            InlineKeyboardButton("🤝 Последствия", callback_data="The_Era_of_Unification_The_Consequences"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_aikatsu")
        )
        return markup

    @staticmethod
    def introduction_state_aikatsu_The_Age_of_Floating_Gates():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🌍 Внешние угрозы", callback_data="The_Age_of_Floating_Gates_External_threats"),
            InlineKeyboardButton("⚡ Внутренний конфликт", callback_data="The_Age_of_Floating_Gates_Internal_conflict"),
            InlineKeyboardButton("🏛️ Политическое напряжение", callback_data="The_Age_of_Floating_Gates_Political_tension"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_aikatsu")
        )
        return markup

    @staticmethod
    def introduction_state_description_Northern_Silence():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("❄️ Эпоха живого севера", callback_data="The_Era_of_the_Living_North"),
            InlineKeyboardButton("🌑 Эпоха Второго Падения Солнца", callback_data="The_Era_of_the_Second_Fall_of_the_Sun"),
            InlineKeyboardButton("🌌 Эпоха Статичного Неба", callback_data="The_Era_of_the_Stationary_Sky"),
            InlineKeyboardButton("🚶 Эпоха Медленного Похода", callback_data="The_Era_of_the_Slow_Procession"),
            InlineKeyboardButton("✅ Выбрать Северное Молчание", callback_data="select_state_Northern_Silence"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection")
        )
        return markup

    @staticmethod
    def introduction_state_Northern_Silence_The_Era_of_the_Living_North():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🎭 Культура", callback_data="The_Era_of_the_Living_North_Culture"),
            InlineKeyboardButton("⚔️ Конфликты", callback_data="The_Era_of_the_Living_North_Conflicts"),
            InlineKeyboardButton("🔮 Магия и вера", callback_data="The_Era_of_the_Living_North_Magic_and_Faith"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Northern_Silence")
        )
        return markup

    @staticmethod
    def introduction_state_Northern_Silence_The_Era_of_the_Second_Sun_Fall():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("💥 Катастрофа", callback_data="The_Era_of_the_Second_Sun_Fall_Catastrophe"),
            InlineKeyboardButton("👑 Преображение Мириэль", callback_data="The_Era_of_the_Second_Sun_Fall_Miriel_Transformation"),
            InlineKeyboardButton("🌍 Реакция мира", callback_data="The_Era_of_the_Second_Sun_Fall_World_Reaction"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Northern_Silence")
        )
        return markup

    @staticmethod
    def introduction_state_Northern_Silence_The_Era_of_the_Stationary_Sky():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🏙️ Жизнь в статике", callback_data="The_Era_of_the_Stationary_Sky_Life_in_Static"),
            InlineKeyboardButton("❄️ Арктик-маги", callback_data="The_Era_of_the_Stationary_Sky_Arctic_Mages"),
            InlineKeyboardButton("📜 Известные фигуры", callback_data="The_Era_of_the_Stationary_Sky_Notable_Figures"),
            InlineKeyboardButton("⚖️ Внутренние трения", callback_data="The_Era_of_the_Stationary_Sky_Internal_Tensions"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Northern_Silence")
        )
        return markup

    @staticmethod
    def introduction_state_Northern_Silence_The_Era_of_the_Slow_Procession():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🗺️ Внешняя экспансия", callback_data="The_Era_of_the_Slow_Procession_External_Expansion"),
            InlineKeyboardButton("📖 Идеология похода", callback_data="The_Era_of_the_Slow_Procession_Ideology_of_the_Procession"),
            InlineKeyboardButton("⚔️ Конфликты с другими силами", callback_data="The_Era_of_the_Slow_Procession_Conflicts_with_Other_Forces"),
            InlineKeyboardButton("👥 Предатели и сомневающиеся", callback_data="The_Era_of_the_Slow_Procession_Traitors_and_Doubters"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Northern_Silence")
        )
        return markup

    @staticmethod
    def introduction_state_description_Burning_Limit():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🔥 Эпоха Пепельных Королевств", callback_data="The_Era_of_the_Ashen_Kingdoms"),
            InlineKeyboardButton("⚔️ Эпоха Восстания Пламени", callback_data="The_Era_of_the_Fire_Rebellion"),
            InlineKeyboardButton("👑 Эпоха Железного Правления", callback_data="The_Era_of_the_Iron_Rule"),
            InlineKeyboardButton("🗺️ Эпоха Похода к Долине", callback_data="bl5"),
            InlineKeyboardButton("✅ Выбрать Пылающий Предел", callback_data="select_state_Burning_Limit"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection")
        )
        return markup

    @staticmethod
    def introduction_state_description_4():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("✅ Выбрать Дварфов", callback_data="select_state_4"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection")
        )
        return markup

    @staticmethod
    def introduction_state_Burning_The_Era_of_the_Ashen_Kingdoms():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🎭 Культура", callback_data="The_Era_of_the_Ashen_Kingdoms_Culture"),
            InlineKeyboardButton("⚔️ Конфликты", callback_data="The_Era_of_the_Ashen_Kingdoms_Conflicts"),
            InlineKeyboardButton("⚔️ Магия и воины", callback_data="The_Era_of_the_Ashen_Kingdoms_Magic_and_Warriors"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Burning_Limit")
        )
        return markup

    @staticmethod
    def introduction_state_Burning_The_Era_of_the_Fire_Rebellion():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📈 Возвышение Хомусуби", callback_data="The_Era_of_the_Fire_Rebellion_The_Rise_of_Homusubi"),
            InlineKeyboardButton("🏚️ Слом старых королевств", callback_data="The_Era_of_the_Fire_Rebellion_The_Fall_of_the_Old_Kingdoms"),
            InlineKeyboardButton("🛡️ Рождение особой гвардии", callback_data="The_Era_of_the_Fire_Rebellion_The_Birth_of_the_Special_Guard"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Burning_Limit")
        )
        return markup

    @staticmethod
    def introduction_state_Burning_The_Era_of_the_Iron_Rule():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🏛️ Общество и контроль", callback_data="The_Era_of_the_Iron_Rule_Society_and_Control"),
            InlineKeyboardButton("🗡️ Ассасины как сущность Предела", callback_data="The_Era_of_the_Iron_Rule_Assassins_as_a_Pillar_of_the_Limit"),
            InlineKeyboardButton("📜 Известные ассасины", callback_data="The_Era_of_the_Iron_Rule_Famous_Assassins"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Burning_Limit")
        )
        return markup

    @staticmethod
    def ISB_The_Era_of_the_Exp_to_the_Valley():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🎯 Стратегическая цель", callback_data="The_Era_of_the_Exp_to_the_Vall_Strat_Obj"),
            InlineKeyboardButton("🛡️ Роль особой гвардии", callback_data="The_Era_of_the_Exp_to_the_Valley_Spec_Guard_and_Assas_Rol"),
            InlineKeyboardButton("🔥 Идеология экспансии", callback_data="The_Era_of_the_Exp_to_the_Valley_Ideol_of_Exp"),
            InlineKeyboardButton("⬅️ Назад", callback_data="state_selection_Burning_Limit")
        )
        return markup

    @staticmethod
    def introduction_class_selection():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🧙 Маг", callback_data="class_selection_1"),
            InlineKeyboardButton("🛡️ Рыцарь", callback_data="class_selection_2"),
            InlineKeyboardButton("🏹 Лучник", callback_data="class_selection_3"),
            InlineKeyboardButton("🗡️ Ассасин", callback_data="class_selection_4")
        )
        return markup

    @staticmethod
    def introduction_class_description_1():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("✅ Выбрать", callback_data="select_class_1"), InlineKeyboardButton("⬅️ Назад", callback_data="class_selection"))
        return markup

    @staticmethod
    def introduction_class_description_2():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("✅ Выбрать", callback_data="select_class_2"), InlineKeyboardButton("⬅️ Назад", callback_data="class_selection"))
        return markup

    @staticmethod
    def introduction_class_description_3():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("✅ Выбрать", callback_data="select_class_3"), InlineKeyboardButton("⬅️ Назад", callback_data="class_selection"))
        return markup

    @staticmethod
    def introduction_class_description_4():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("✅ Выбрать", callback_data="select_class_4"), InlineKeyboardButton("⬅️ Назад", callback_data="class_selection"))
        return markup

    @staticmethod
    def profile_1():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("⚡ Навыки", callback_data="profile_skills"),
            InlineKeyboardButton("🗑️ Удалить профиль", callback_data="profile_delete_confirm"),
            InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu")
        )
        return markup

    @staticmethod
    def profile_class():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="profile_class_back"))
        return markup

    @staticmethod
    def profile_subclass():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="profile_subclass_back"))
        return markup

    @staticmethod
    def profile_delete_confirm():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("✅ Да", callback_data="profile_delete_yes"), InlineKeyboardButton("❌ Нет", callback_data="profile_delete_no"))
        return markup

    @staticmethod
    def battle_keyboard():
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⚔️ Атаковать", callback_data="battle_attack"),
            InlineKeyboardButton("🛡️ Защищаться", callback_data="battle_defend"),
            InlineKeyboardButton("🏃 Убежать", callback_data="battle_flee"),
            InlineKeyboardButton("📜 История боя", callback_data="battle_log")
        )
        return markup