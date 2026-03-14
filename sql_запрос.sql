-- Удаление таблиц, если они существуют (в правильном порядке с учетом зависимостей)
DROP TABLE IF EXISTS "Inventory", "Items", "Battles", "ActiveQuests", "Quests", "Skills", "Monsters", "Locations", "Users", "Subclasses", "EpochDetails", "Epochs", "States", "Classes", "ClassProsCons", "FamousCharacters";

-- Таблица States (Государства) - расширяем
CREATE TABLE "States" (
    state_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    emblem VARCHAR(100),
    color VARCHAR(20),
    leader_title VARCHAR(100)
);

-- Таблица Classes (Классы) - расширяем
CREATE TABLE "Classes" (
    class_id SERIAL PRIMARY KEY,
    state_id INT NOT NULL REFERENCES "States"(state_id),
    name VARCHAR(100) NOT NULL,
    type_damage VARCHAR(50) NOT NULL,
    description TEXT,
    base_hp INT NOT NULL DEFAULT 100,
    base_mana INT NOT NULL DEFAULT 50,
    base_damage INT NOT NULL DEFAULT 10,
    base_defence INT NOT NULL DEFAULT 5,
    special_ability VARCHAR(100)
);

-- Таблица Subclasses (Подклассы/Специализации)
CREATE TABLE "Subclasses" (
    subclass_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL REFERENCES "Classes"(class_id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    bonus_damage INT DEFAULT 0,
    bonus_defence INT DEFAULT 0,
    bonus_hp INT DEFAULT 0,
    bonus_mana INT DEFAULT 0
);

-- Таблица Epochs (Эпохи/Периоды игры)
CREATE TABLE "Epochs" (
    epoch_id SERIAL PRIMARY KEY,
    state_id INT NOT NULL REFERENCES "States"(state_id),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL
);

-- Таблица EpochDetails (Детали эпох)
CREATE TABLE "EpochDetails" (
    epoch_details_id SERIAL PRIMARY KEY,
    epoch_id INT NOT NULL REFERENCES "Epochs"(epoch_id),
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL
);

-- Таблица Locations (Локации)
CREATE TABLE "Locations" (
    location_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    required_level INT NOT NULL DEFAULT 1,
    state_id INT REFERENCES "States"(state_id),
    location_type VARCHAR(50) NOT NULL,
    min_level_monsters INT DEFAULT 1,
    max_level_monsters INT DEFAULT 5
);

-- Таблица Users (Пользователи/Персонажи) - расширяем
CREATE TABLE "Users" (
    user_id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    lvl INT NOT NULL DEFAULT 1,
    experience_now INT NOT NULL DEFAULT 0,
    experience_future INT NOT NULL DEFAULT 100,
    hp INT NOT NULL DEFAULT 100,
    max_hp INT NOT NULL DEFAULT 100,
    mana INT DEFAULT 50,
    max_mana INT DEFAULT 50,
    damage INT NOT NULL DEFAULT 10,
    defence INT NOT NULL DEFAULT 5,
    agility INT NOT NULL DEFAULT 5,
    star_coin BIGINT NOT NULL DEFAULT 0,
    skill_point INT NOT NULL DEFAULT 0,
    class_id INT NOT NULL REFERENCES "Classes"(class_id),
    subclass_id INT NOT NULL REFERENCES "Subclasses"(subclass_id),
    state_id INT NOT NULL REFERENCES "States"(state_id),
    location_id INT NOT NULL REFERENCES "Locations"(location_id),
    stealth INT DEFAULT 0,
    illusion_power INT DEFAULT 0,
    current_hp INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица Skills (Навыки)
CREATE TABLE "Skills" (
    skill_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL REFERENCES "Classes"(class_id),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    damage INT NOT NULL DEFAULT 0,
    mana_cost INT NOT NULL DEFAULT 0,
    cooldown INT NOT NULL DEFAULT 1,
    level_required INT NOT NULL DEFAULT 1,
    skill_type VARCHAR(50) NOT NULL
);

-- Таблица Monsters (Монстры)
CREATE TABLE "Monsters" (
    monster_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INT NOT NULL DEFAULT 1,
    hp INT NOT NULL,
    damage INT NOT NULL,
    defence INT NOT NULL,
    experience_reward INT NOT NULL,
    star_coin_reward INT NOT NULL,
    location_id INT NOT NULL REFERENCES "Locations"(location_id),
    monster_type VARCHAR(50) NOT NULL
);

-- Таблица Items (Предметы)
CREATE TABLE "Items" (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    rarity VARCHAR(20) NOT NULL,
    required_level INT NOT NULL DEFAULT 1,
    damage_bonus INT DEFAULT 0,
    defence_bonus INT DEFAULT 0,
    hp_bonus INT DEFAULT 0,
    mana_bonus INT DEFAULT 0,
    agility_bonus INT DEFAULT 0,
    price INT NOT NULL DEFAULT 0
);

-- Таблица Inventory (Инвентарь)
CREATE TABLE "Inventory" (
    inventory_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "Users"(user_id),
    item_id INT NOT NULL REFERENCES "Items"(item_id),
    quantity INT NOT NULL DEFAULT 1,
    equipped BOOLEAN NOT NULL DEFAULT FALSE
);

-- Таблица Quests (Квесты)
CREATE TABLE "Quests" (
    quest_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    required_level INT NOT NULL DEFAULT 1,
    reward_experience INT NOT NULL,
    reward_star_coin INT NOT NULL,
    reward_item_id INT REFERENCES "Items"(item_id),
    quest_type VARCHAR(50) NOT NULL,
    state_id INT REFERENCES "States"(state_id),
    location_id INT REFERENCES "Locations"(location_id)
);

-- Таблица ActiveQuests (Активные квесты)
CREATE TABLE "ActiveQuests" (
    active_quest_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "Users"(user_id),
    quest_id INT NOT NULL REFERENCES "Quests"(quest_id),
    progress INT NOT NULL DEFAULT 0,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица Battles (Бои)
CREATE TABLE "Battles" (
    battle_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES "Users"(user_id),
    monster_id INT REFERENCES "Monsters"(monster_id),
    battle_type VARCHAR(50) NOT NULL,
    result VARCHAR(10) NOT NULL,
    experience_gained INT NOT NULL,
    star_coin_gained INT NOT NULL,
    battle_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    battle_log TEXT
);

-- Создаем таблицу для плюсов/минусов классов
CREATE TABLE "ClassProsCons" (
    pros_cons_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL REFERENCES "Classes"(class_id),
    type VARCHAR(10) NOT NULL CHECK (type IN ('pro', 'con')),
    description TEXT NOT NULL
);

-- Создаем таблицу для известных персонажей
CREATE TABLE "FamousCharacters" (
    famous_character_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL REFERENCES "Classes"(class_id),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    ability_description TEXT
);