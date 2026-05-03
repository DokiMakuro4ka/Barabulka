    -- ==========================================
    -- RESET СХЕМЫ (для миграций dev-окружения)
    -- ==========================================

    DROP TABLE IF EXISTS
        "Inventory",
        "Items",
        "Battles",
        "ActiveQuests",
        "Quests",
        "Skills",
        "Monsters",
        "Locations",
        "Users",
        "Subclasses",
        "EpochDetails",
        "Epochs",
        "States",
        "Classes",
        "ClassProsCons",
        "FamousCharacters";

    -- ==========================================
    -- 1. СПРАВОЧНИКИ / ЛОР (data + engine/world)
    -- ==========================================

    -- Государства / фракции верхнего уровня
    CREATE TABLE "States" (
        state_id      SERIAL PRIMARY KEY,
        name          VARCHAR(100) NOT NULL,
        description   TEXT NOT NULL,
        emblem        VARCHAR(100),
        color         VARCHAR(20),
        leader_title  VARCHAR(100)
    );

    -- Классы персонажей (глобальные, могут быть доступны во всех государствах)
    CREATE TABLE "Classes" (
        class_id       SERIAL PRIMARY KEY,
        state_id       INT REFERENCES "States"(state_id),  -- опционально: спец-класс только для конкретного гос-ва
        name           VARCHAR(100) NOT NULL,
        type_damage    VARCHAR(50) NOT NULL,               -- physical / magic / hybrid
        description    TEXT,
        base_hp        INT NOT NULL DEFAULT 100,
        base_mana      INT NOT NULL DEFAULT 50,
        base_damage    INT NOT NULL DEFAULT 10,
        base_defence   INT NOT NULL DEFAULT 5,
        special_ability VARCHAR(100)
    );

    -- Подклассы / специализации
    CREATE TABLE "Subclasses" (
        subclass_id    SERIAL PRIMARY KEY,
        class_id       INT NOT NULL REFERENCES "Classes"(class_id),
        name           VARCHAR(100) NOT NULL,
        description    TEXT,
        bonus_damage   INT DEFAULT 0,
        bonus_defence  INT DEFAULT 0,
        bonus_hp       INT DEFAULT 0,
        bonus_mana     INT DEFAULT 0
    );

    -- Эпохи (лоровые состояния мира по гос-ву)
    CREATE TABLE "Epochs" (
        epoch_id       SERIAL PRIMARY KEY,
        state_id       INT NOT NULL REFERENCES "States"(state_id),
        name           VARCHAR(100) NOT NULL,
        description    TEXT NOT NULL
    );

    -- Детали эпох (категории из твоего handler'а: Конфликты, Культура и т.п.)
    CREATE TABLE "EpochDetails" (
        epoch_details_id SERIAL PRIMARY KEY,
        epoch_id         INT NOT NULL REFERENCES "Epochs"(epoch_id),
        category         VARCHAR(50) NOT NULL,
        content          TEXT NOT NULL
    );

    -- Локации мира (engine/world/map, world_repo)
    CREATE TABLE "Locations" (
        location_id        SERIAL PRIMARY KEY,
        name               VARCHAR(100) NOT NULL,
        description        TEXT NOT NULL,
        required_level     INT NOT NULL DEFAULT 1,
        state_id           INT REFERENCES "States"(state_id),
        location_type      VARCHAR(50) NOT NULL,          -- capital / dungeon / wild / city ...
        min_level_monsters INT DEFAULT 1,
        max_level_monsters INT DEFAULT 5
    );

    -- Навыки (engine/skills, data/skills.py)
    CREATE TABLE "Skills" (
        skill_id       SERIAL PRIMARY KEY,
        class_id       INT NOT NULL REFERENCES "Classes"(class_id),
        name           VARCHAR(100) NOT NULL,
        description    TEXT NOT NULL,
        damage         INT NOT NULL DEFAULT 0,
        mana_cost      INT NOT NULL DEFAULT 0,
        cooldown       INT NOT NULL DEFAULT 1,
        level_required INT NOT NULL DEFAULT 1,
        skill_type     VARCHAR(50) NOT NULL          -- active / passive / ultimate ...
    );

    -- Типы монстров (шаблоны монстров)
    CREATE TABLE "Monsters" (
        monster_id        SERIAL PRIMARY KEY,
        name              VARCHAR(100) NOT NULL,
        level             INT NOT NULL DEFAULT 1,
        hp                INT NOT NULL,
        damage            INT NOT NULL,
        defence           INT NOT NULL,
        experience_reward INT NOT NULL,
        star_coin_reward  INT NOT NULL,
        location_id       INT NOT NULL REFERENCES "Locations"(location_id),
        monster_type      VARCHAR(50) NOT NULL         -- beast / elemental / undead ...
    );

    -- Предметы (item templates)
    CREATE TABLE "Items" (
        item_id        SERIAL PRIMARY KEY,
        name           VARCHAR(100) NOT NULL,
        description    TEXT NOT NULL,
        item_type      VARCHAR(50) NOT NULL,           -- weapon / armor / consumable / quest ...
        rarity         VARCHAR(20) NOT NULL,           -- common / rare / epic / legendary
        required_level INT NOT NULL DEFAULT 1,
        damage_bonus   INT DEFAULT 0,
        defence_bonus  INT DEFAULT 0,
        hp_bonus       INT DEFAULT 0,
        mana_bonus     INT DEFAULT 0,
        agility_bonus  INT DEFAULT 0,
        price          INT NOT NULL DEFAULT 0
    );

    -- Плюсы/минусы классов (для UI выбора класса)
    CREATE TABLE "ClassProsCons" (
        pros_cons_id  SERIAL PRIMARY KEY,
        class_id      INT NOT NULL REFERENCES "Classes"(class_id),
        type          VARCHAR(10) NOT NULL CHECK (type IN ('pro', 'con')),
        description   TEXT NOT NULL
    );

    -- Известные персонажи (лоровые NPC, могут мапиться на engine/entities/npc.py)
    CREATE TABLE "FamousCharacters" (
        famous_character_id SERIAL PRIMARY KEY,
        class_id            INT NOT NULL REFERENCES "Classes"(class_id),
        name                VARCHAR(100) NOT NULL,
        description         TEXT NOT NULL,
        ability_description TEXT
    );

    -- ==========================================
    -- 2. ПЕРСИСТЕНТНОЕ СОСТОЯНИЕ ИГРОКА / МИРА
    -- ==========================================

    -- Пользователь / персонаж (player entity)
    CREATE TABLE "Users" (
        user_id         SERIAL PRIMARY KEY,
        telegram_id     BIGINT UNIQUE NOT NULL,          -- связь с Telegram
        name            VARCHAR(100) NOT NULL,
        lvl             INT NOT NULL DEFAULT 1,
        experience_now  INT NOT NULL DEFAULT 0,
        experience_future INT NOT NULL DEFAULT 100,
        hp              INT NOT NULL DEFAULT 100,
        max_hp          INT NOT NULL DEFAULT 100,
        mana            INT DEFAULT 50,
        max_mana        INT DEFAULT 50,
        damage          INT NOT NULL DEFAULT 10,
        defence         INT NOT NULL DEFAULT 5,
        agility         INT NOT NULL DEFAULT 5,
        star_coin       BIGINT NOT NULL DEFAULT 0,
        skill_point     INT NOT NULL DEFAULT 0,
        class_id        INT NOT NULL REFERENCES "Classes"(class_id),
        subclass_id     INT NOT NULL REFERENCES "Subclasses"(subclass_id),
        state_id        INT NOT NULL REFERENCES "States"(state_id),
        location_id     INT NOT NULL REFERENCES "Locations"(location_id),
        stealth         INT DEFAULT 0,
        illusion_power  INT DEFAULT 0,
        current_hp      INT NOT NULL DEFAULT 100,
        created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Инвентарь конкретного игрока
    CREATE TABLE "Inventory" (
        inventory_id SERIAL PRIMARY KEY,
        user_id      INT NOT NULL REFERENCES "Users"(user_id),
        item_id      INT NOT NULL REFERENCES "Items"(item_id),
        quantity     INT NOT NULL DEFAULT 1,
        equipped     BOOLEAN NOT NULL DEFAULT FALSE
    );

    -- Квесты (описания)
    CREATE TABLE "Quests" (
        quest_id          SERIAL PRIMARY KEY,
        title             VARCHAR(200) NOT NULL,
        description       TEXT NOT NULL,
        required_level    INT NOT NULL DEFAULT 1,
        reward_experience INT NOT NULL,
        reward_star_coin  INT NOT NULL,
        reward_item_id    INT REFERENCES "Items"(item_id),
        quest_type        VARCHAR(50) NOT NULL,       -- main / side / faction / daily ...
        state_id          INT REFERENCES "States"(state_id),
        location_id       INT REFERENCES "Locations"(location_id)
    );

    -- Активные квесты игрока (quest progress)
    CREATE TABLE "ActiveQuests" (
        active_quest_id SERIAL PRIMARY KEY,
        user_id         INT NOT NULL REFERENCES "Users"(user_id),
        quest_id        INT NOT NULL REFERENCES "Quests"(quest_id),
        progress        INT NOT NULL DEFAULT 0,
        completed       BOOLEAN NOT NULL DEFAULT FALSE,
        started_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Бои (лог для battle_repo + статистика)
    CREATE TABLE "Battles" (
        battle_id         SERIAL PRIMARY KEY,
        user_id           INT NOT NULL REFERENCES "Users"(user_id),
        monster_id        INT REFERENCES "Monsters"(monster_id),
        battle_type       VARCHAR(50) NOT NULL,        -- pve / pvp / boss / event
        result            VARCHAR(10) NOT NULL,        -- win / lose / flee
        experience_gained INT NOT NULL,
        star_coin_gained  INT NOT NULL,
        battle_date       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        battle_log        TEXT                          -- сериализованный лог боя для analytics/debug
    );

    -- ========================================
    -- НАЧАЛЬНЫЕ ДАННЫЕ ПО ЛОРУ
    -- ========================================

    -- 1. Государства
    INSERT INTO "States" (state_id, name, description, emblem, color, leader_title) VALUES
        (1, 'Айкацу',
        'Государство воздушной магии, центр дисциплины и гармонии ветра.',
        'aikatsu_emblem', '#88ccff', 'Владыка Ветра'),
        (2, 'Северное Молчание',
        'Государство льда и статики, где время почти остановлено.',
        'north_silence_emblem', '#ddeeff', 'Белая Тишина'),
        (3, 'Пылающий Предел',
        'Империя огня, железной дисциплины и жестокой военной машины.',
        'burning_limit_emblem', '#ff5500', 'Огненный Император'),
        (4, 'Дварфы',
        'Горное королевство, мастера металла и крепких тел.',
        'dwarves_emblem', '#ccaa66', 'Верховный кузнец')
    ON CONFLICT (state_id) DO NOTHING;

    -- 2. Базовые классы (глобальные, без привязки к конкретному state)
    INSERT INTO "Classes" (class_id, name, type_damage, description,
                        base_hp, base_mana, base_damage, base_defence, special_ability)
    VALUES
        (1, 'Маг',     'magic',
        'Мастер стихий и заклинаний, наносит дистанционный магический урон.',
        80, 150, 15, 3, 'Сильная AoE магия'),
        (2, 'Рыцарь',  'physical',
        'Бронированный воин ближнего боя, выдерживает большое количество ударов.',
        150, 50, 12, 10, 'Мощные защитные стойки'),
        (3, 'Лучник',  'physical',
        'Дальний бой, высокая точность и мобильность.',
        100, 60, 14, 5, 'Критические выстрелы'),
        (4, 'Ассасин', 'physical',
        'Скрытный убийца с сильным взрывным уроном по одиночной цели.',
        90, 70, 18, 4, 'Атаки из тени с повышенным уроном')
    ON CONFLICT (class_id) DO NOTHING;

    -- 3. Примеры подклассов
    INSERT INTO "Subclasses" (class_id, name, description, bonus_damage, bonus_defence, bonus_hp, bonus_mana) VALUES
        (1, 'Архимаг',   'Специализация на мощных стихиях и контроле поля боя.', 5, 0, 0, 30),
        (2, 'Защитник',  'Максимальная стойкость и защита союзников.', 0, 5, 30, 0),
        (3, 'Снайпер',   'Повышенный урон по одиночной цели с большой дистанции.', 7, 0, 0, 0),
        (4, 'Теневой клинок', 'Ассасин, специализирующийся на критах из невидимости.', 8, 0, 0, 0);

    -- 4. Базовые локации
    INSERT INTO "Locations" (location_id, name, description, required_level, state_id,
                            location_type, min_level_monsters, max_level_monsters)
    VALUES
        (1, 'Главный остров Айкацу',
        'Парящий остров, где расположен Небесный Додзё и совет магов ветра.',
        1, 1, 'capital', 1, 5),
        (2, 'Столичный город Северного Молчания',
        'Геометрически выверенный город статики под наблюдением Белой Тишины.',
        1, 2, 'capital', 1, 5),
        (3, 'Цитадель Пылающего Предела',
        'Крепость из чёрного камня и огня, резиденция Огненного Императора.',
        1, 3, 'capital', 1, 5),
        (4, 'Главный город Дварфов',
        'Горный мегаполис кузниц и таверн, вырубленный в скале.',
        1, 4, 'capital', 1, 5)
    ON CONFLICT (location_id) DO NOTHING;

    -- 5. Эпохи Айкацу (state_id = 1)
    INSERT INTO "Epochs" (epoch_id, state_id, name, description) VALUES
        (1, 1, 'Эпоха Тумана',
        'Период, когда Айкацу формировался среди магических туманов и конфликтов кланов.'),
        (2, 1, 'Эпоха Объединения',
        'Время Хосэя, великого маг‑самурая, который объединил кланы и создал Кодекс Воздуха.'),
        (3, 1, 'Эпоха Парящих Врат',
        'Период воздушных технологий, парящих храмов и политического раскола.')
    ON CONFLICT (epoch_id) DO NOTHING;

    INSERT INTO "EpochDetails" (epoch_id, category, content) VALUES
        (1, 'Конфликты',
        'Кланы Айкацу вели затяжные войны, а магический туман скрывал истинные намерения союзников и врагов.'),
        (1, 'Культура',
        'Общины жили в гармонии с туманом, создавая ритуалы, усиливающие связь с воздухом и предками.'),
        (2, 'Кодекс Воздуха',
        'Хосэй создал свод правил: Чистота Намерения, Тишина Сердца, Сила Без Гнева, Путь Ветра, Честь Движения, Защита Слабого, Гармония Стихий.'),
        (2, 'Небесный Додзё',
        'На центральном острове построен храм, где обучали четырём путям: Клинок (Фуусин), Дыхание (Камино), Туман (Кагэноха), Щит (Сораносеки).'),
        (2, 'Последствия',
        'Кланы приняли общую структуру, магия стала инструментом баланса, началась эпоха дипломатии и духовного роста.'),
        (3, 'Общее описание',
        'Айкацу стал центром воздушной магии, развились парящие библиотеки, храмы и мосты из ветра.'),
        (3, 'Внешние угрозы',
        'Государства Огня и Земли стремятся проникнуть в Долину Природы, Айкацу защищает её как священный источник равновесия.'),
        (3, 'Внутренний конфликт',
        'Традиционалисты верны Кодексу и пути просветления, новаторы хотят использовать магию для прогресса и оружия.'),
        (3, 'Политическое напряжение',
        'Совет расколот, появляются тайные школы, некоторые маги ищут союзы с другими стихиями.')
    ON CONFLICT DO NOTHING;

    -- 6. Эпохи Северного Молчания (state_id = 2)
    INSERT INTO "Epochs" (epoch_id, state_id, name, description) VALUES
        (4, 2, 'Эпоха Живого Севера',
        'Север до Второго Падения Солнца: суровый, но живой мир циклов льда и оттепелей.'),
        (5, 2, 'Эпоха Второго Падения Солнца',
        'Катастрофа, запустившая Статику и вечную зиму.'),
        (6, 2, 'Эпоха Статичного Неба',
        'Время тотального контроля и геометрически выверенных городов статики.'),
        (7, 2, 'Эпоха Медленного Похода',
        'Медленное наступление льда на юг, к Долине Природы.')
    ON CONFLICT (epoch_id) DO NOTHING;

    INSERT INTO "EpochDetails" (epoch_id, category, content) VALUES
        (4, 'Культура',
        'Северяне почитали циклы смены льда и оттепелей, проводили праздники первой оттепели и последнего снега, музыка имитировала треск льда и шум волн.'),
        (4, 'Конфликты',
        'Главные конфликты — споры за рыбу, меха и безопасные пути, локальные войны завершались Ночью Перемирия у общего костра.'),
        (4, 'Магия и вера',
        'Маги усиливали движение ветров и снегопадов, вера считала любой застой признаком болезни мира.'),
        (5, 'Катастрофа',
        'Свет стал тускнеть, тени вытянулись и застыли, небо застыло между рассветом и закатом, время стекало в трещины льда.'),
        (5, 'Преображение Мириэль',
        'Королева Мириэль провела запретный ритуал соединения сознания с атмосферой и кристаллическим светом, став Белой Тишиной.'),
        (5, 'Реакция мира',
        'Часть подданных увидела спасение, другие — тиранию статики и пытались бежать на юг.'),
        (6, 'Жизнь в статике',
        'Время измеряется степенью неподвижности, города геометрически совершенны, движение строго регламентировано.'),
        (6, 'Арктик-маги',
        'Арктик-маги переписывают физику пространства, их способность "Кристаллизация Реальности" подчиняет движение ритму сердца.'),
        (6, 'Известные фигуры',
        'Мириэль как распределённое сознание статики, Аэллар, Монах Фракталов, создаёт зеркальные структуры, отражающие удары и намерения.'),
        (6, 'Внутренние трения',
        'Одни находят покой в предсказуемости, другие страдают от исчезновения радости, творчества и любви.'),
        (7, 'Внешняя экспансия',
        'Северное Молчание начинает "поход без маршей": медленное, но неуклонное продвижение льда к Долине Природы.'),
        (7, 'Идеология похода',
        'Мириэль убеждена, что остановка живой Долины — милосердие и защита от нового Падения.'),
        (7, 'Конфликты с другими силами',
        'На границах статика льда сталкивается с магией ветра, пламенем и живой землёй, рождая искажённые зоны.'),
        (7, 'Предатели и сомневающиеся',
        'Тарин, Клятвопреступник, поверил в спасение через остановку; часть магов льда сомневается в ценности вечной статики.')
    ON CONFLICT DO NOTHING;

    -- 7. Эпохи Пылающего Предела (state_id = 3)
    INSERT INTO "Epochs" (epoch_id, state_id, name, description) VALUES
        (8, 3, 'Эпоха Пепельных Королевств',
        'Разрозненные огненные королевства, войны за тепло и металл среди обугленных земель.'),
        (9, 3, 'Эпоха Восстания Пламени',
        'Подъём Хомусуби и объединение королевств в Пылающий Предел.'),
        (10, 3, 'Эпоха Железного Правления',
        'Государство вечного жара, дисциплины и страха, где каждый — ресурс для пламени.'),
        (11, 3, 'Эпоха Похода к Долине',
        'Современный период внешней экспансии Предела к Долине Природы.')
    ON CONFLICT (epoch_id) DO NOTHING;

    INSERT INTO "EpochDetails" (epoch_id, category, content) VALUES
        (8, 'Культура',
        'Люди жили в небольших королевствах и кланах, культ огня был разрозненным и связанным с выживанием после пожаров и извержений.'),
        (8, 'Конфликты',
        'Основные войны велись за источники тепла, металл и безопасные пути, единого врага не было.'),
        (8, 'Магия и воины',
        'Одни кланы делали ставку на тяжёлую пехоту, другие на быстрых налётчиков, убийцы использовали огонь как прикрытие.'),
        (9, 'Возвышение Хомусуби',
        'Хомусуби собрал недовольных междоусобицами и предложил идею единого Предела, властвующего через закон огня и страх.'),
        (9, 'Слом старых королевств',
        'Старые династии были уничтожены или ассимилированы, их символы сожжены в огненных ритуалах, покорные города стали военными центрами.'),
        (9, 'Рождение особой гвардии',
        'Создано закрытое братство особой гвардии, из которого выросли ассасины Предела — инструмент тайного устранения врагов.'),
        (10, 'Общество и контроль',
        'Дисциплина и страх — основа жизни, слабость считается преступлением, дети с ранних лет обучаются выносливости и бою.'),
        (10, 'Ассасины как опора Предела',
        'Ассасины — воплощение идеи огня, прожигающего препятствия изнутри, их стиль сочетает скорость, выносливость и абсолютный контроль.'),
        (10, 'Известные ассасины',
        'Момоти с кусаригамой, Кенджи с парой кинжалов, Сакато с кастетами и чужеземец Джейкоб с тяжёлой катаной.'),
        (11, 'Стратегическая цель',
        'Официальная и скрытая цель Предела — захват и подчинение Долины Природы как ключа к ресурсам и символу окончательной победы огня.'),
        (11, 'Роль особой гвардии и ассасинов',
        'Особая гвардия и ассасины Предела отправляются в Долину и соседние регионы с задачами устранения лидеров сопротивления, подрыва доверия между фракциями и создания ощущения неизбежности победы огня. Они действуют как тень Императора: никто не знает, где они появятся, но каждый понимает, что любой, кто встанет на пути Хомусуби, может исчезнуть в пламени без следа.'),
        (11, 'Идеология экспансии',
        'С точки зрения Предела, мир должен либо сгореть, либо преклониться перед огнём: тот, кто не выдерживает жара, не достоин выживания. Пылающий Предел убеждён, что только тот, кто живёт на грани боли и смерти, имеет право диктовать условия остальному миру.')
    ON CONFLICT DO NOTHING;

    -- Начальные монстры для каждой локации
    INSERT INTO "Monsters" (name, level, hp, damage, defence, experience_reward, star_coin_reward, location_id, monster_type) VALUES
    -- Локация 1 (Айкацу)
    ('Гоблин', 1, 40, 10, 3, 50, 10, 1, 'beast'),
    ('Волк', 1, 35, 12, 2, 45, 8, 1, 'beast'),
    ('Разбойник', 2, 45, 14, 4, 60, 15, 1, 'humanoid'),
    -- Локация 2 (Северное Молчание)
    ('Снежный волк', 1, 45, 11, 3, 55, 12, 2, 'beast'),
    ('Ледяной голем', 2, 70, 15, 6, 90, 20, 2, 'elemental'),
    -- Локация 3 (Пылающий Предел)
    ('Огненный бес', 1, 38, 12, 2, 48, 9, 3, 'demon'),
    ('Пепельный элементаль', 2, 55, 16, 4, 75, 16, 3, 'elemental'),
    -- Локация 4 (Дварфы)
    ('Каменный скорпион', 1, 50, 9, 6, 50, 11, 4, 'beast'),
    ('Тролль-шахтёр', 2, 80, 12, 7, 95, 22, 4, 'giant')
    ON CONFLICT (monster_id) DO NOTHING;