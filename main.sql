drop table if exists Users, Сlasses, Subclasses, Locations, Inventory, Items, Damage_types, Enemies;

--таблицы подклассов, тоже самое, что и классы, только немного углублённое
create table Subclasses (
	ID_subclass serial primary key,
	--название подкласса
    name varchar(30) not null
);

-- Таблица типов урона
create table Damage_types (
    ID_damage_type serial primary key,
    -- Название типа урона (например, физический, магический, огненный и т.д.)
    name varchar(30) not null
);

-- Таблица классов
create table Сlasses (
    ID_class serial primary key,
    -- Название класса
    name varchar(30) not null,
    -- Внешний ключ на тип урона
    ID_damage_type int not null,
    -- Внешний ключ на подкласс
    ID_subclass int,
	foreign key (ID_damage_type) references Damage_types (ID_damage_type),
    foreign key (ID_subclass) references Subclasses(ID_subclass)
);

--таблицы локаций, здесь предполагается, что будут храниться локаций, названия, описание, доступные квесты, тип локаций(какой биом)
create table Locations (
    ID_location serial primary key,
	--название
    name varchar(40),
	--описание
    description varchar,
	--доступные квесты
    available_quests varchar,
	--тип локаций
    location_type varchar(30)
);

--таблица предметов, здесь буду храниться все предметы и их атрибуты
create table Items (
    ID_item serial primary key,
	--название предмета
    name varchar(65) not null,
	--описание
    description text,
	--редкость
    rarity varchar(20),
	--тип предмета(посох, жезл, ме)
    item_type varchar(20) not null,
	--цена в стар койнах
    price int,
	--главный атрибут
    main_attribute varchar(20)
);

--таблица атрибутов
create table Inventory (
    ID_inventory int primary key,
	--количество предметов
    quantity int,
	--внешний ключ на таблицу предметов
	ID_item int not null,
	foreign key (ID_item) references Items(ID_item)
);

--таблицы игрока
create table Users (
    ID_user int not null,
	--уровень
    lvl int default 0,
	--опыт сейчас, чтобы отображаться опыт на данный момент
    experience_now int default 0,
	--опыт в будущем, чтобы уровень автоматический менялся
    experience_future int default 0,
	--уровень здоровья
    hp int default 0,
	--урон
    damage int default 0,
	--защита
    defence int default 0,
	--ловкость, в основном отвечает за шанс укланения от атаки врага
    agility int default 0,
	--валюта
    star_coin int default 0,
	--внешние ключи
    ID_class int not null,
    ID_subclass int not null,
	ID_inventory int not null,
	foreign key (ID_class) references Сlasses(ID_class),
	foreign key (ID_subclass) references Subclasses(ID_subclass),
	foreign key (ID_inventory) references Inventory(ID_inventory)
);

--таблица врагов
create table Enemies (
    ID_enemy serial primary key,
    --название врага
    name varchar(50) not null,
    --уровень
    lvl int default 1,
    --здоровье
    hp int default 100,
    --урон
    damage int default 10,
    --защита
    defence int default 5,
    --ловкость
    agility int default 5,
    --награда за победу (в стар койнах)
    reward_star_coin int default 50,
    --внешние ключи
    ID_class int not null,
    ID_subclass int not null,
    ID_inventory int not null,
    foreign key (ID_class) references Сlasses(ID_class),
    foreign key (ID_subclass) references Subclasses(ID_subclass),
    foreign key (ID_inventory) references Inventory(ID_inventory)
);