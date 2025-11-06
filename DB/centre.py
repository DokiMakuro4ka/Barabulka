import psycopg2


# Параметры подключения
conn_params = {
    "dbname": "Barabulka",
    "user": "postgres",
    "password": "123123",
    "host": "localhost",
    "port": "5432"
}


class User:
    def get_user(user_id):
        query = f"""SELECT *
                    FROM "Users"
                    WHERE user_id = {user_id}"""
        result = select(query=query)
        return result

    def get_user_text(user_id):
        query = f"""SELECT *
                    FROM "Users"
                    WHERE user_id = {user_id}"""
        user = select(query=query)
        user_class = UserClass.get_class(class_id=user["class_id"])
        user_subclass = UserSubclass.get_subclass(subclass_id=user["subclass_id"])
        user_state = UserState.get_state(state_id=user["state_id"])
        text = f"Профиль (id{user["user_id"]})\n" \
               f"Имя: {user["name"]}\n" \
               f"Государство: {user_state["name"]}\n\n" \
               f"Уровень: {user["lvl"]}\n" \
               f"Опыт: {user["experience_now"]} / {user["experience_future"]}\n\n" \
               f"Класс: {user_class["name"]}\n" \
               f"Подкласс: {user_subclass["name"]}\n\n" \
               f"Здоровье: {user["hp"]}\n" \
               f"Урон: {user["damage"]}\n" \
               f"Защита: {user["defence"]}\n" \
               f"Ловкость: {user["agility"]}\n" \
               f"Очки навыков: {user["skill_point"]}\n" \
               f"Star Коины: {user["star_coin"]}"
        return text

    def set_user_name(user_id, name):
        query = f"""UPDATE "Users"
                    SET name = '{name}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_lvl(user_id, lvl):
        query = f"""UPDATE "Users"
                    SET lvl = '{lvl}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_experience_now(user_id, experience_now):
        query = f"""UPDATE "Users"
                    SET experience_now = '{experience_now}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_experience_future(user_id, experience_future):
        query = f"""UPDATE "Users"
                    SET experience_future = '{experience_future}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_hp(user_id, hp):
        query = f"""UPDATE "Users"
                    SET hp = '{hp}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_damage(user_id, damage):
        query = f"""UPDATE "Users"
                    SET damage = '{damage}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_defence(user_id, defence):
        query = f"""UPDATE "Users"
                    SET defence = '{defence}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_agility(user_id, agility):
        query = f"""UPDATE "Users"
                    SET agility = '{agility}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_star_coin(user_id, star_coin):
        query = f"""UPDATE "Users"
                    SET star_coin = '{star_coin}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_skill_point(user_id, skill_point):
        query = f"""UPDATE "Users"
                    SET skill_coin = '{skill_point}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_class_id(user_id, class_id):
        query = f"""UPDATE "Users"
                    SET class_id = {class_id}
                    WHERE user_id = {user_id};"""
        update(query=query)

    def set_user_subclass_id(user_id, subclass_id):
        query = f"""UPDATE "Users"
                    SET subclass_id = '{subclass_id}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def set_user_state_id(user_id, state_id):
        query = f"""UPDATE "Users"
                    SET state_id = '{state_id}'
                    WHERE user_id = {user_id}"""
        update(query=query)

    def insert_user(user_id, state_id):
        query = f"""INSERT INTO "Users" (user_id, name, lvl, experience_now, experience_future, hp, damage, defence, agility, star_coin, skill_point, class_id, subclass_id, state_id)
                    VALUES ({user_id}, '0', 1, 0, 10, 10, 1, 1, 1, 0, 0, 0, 0, {state_id})"""
        insert(query=query)


class UserClass:
    def get_class(class_id):
        query = f"""SELECT *
                    FROM "Classes"
                    WHERE class_id = {class_id}"""
        result = select(query=query)
        return result


class UserSubclass:
    def get_subclass(subclass_id):
        query = f"""SELECT *
                    FROM "Subclasses"
                    WHERE subclass_id = {subclass_id}"""
        result = select(query=query)
        return result


class UserState:
    def get_state(state_id):
        query = f"""SELECT *
                    FROM "States"
                    WHERE state_id = {state_id}"""
        result = select(query=query)
        return result


class State:
    def get_state(state_id):
        query = f"""SELECT *
                    FROM "States"
                    WHERE state_id = {state_id}"""
        result = select(query=query)
        return result



class Mob:
    pass



def select(query):
    try:
        connection = psycopg2.connect(**conn_params)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))
        return result[0]

    except Exception as error:
        print(f"Ошибка: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def update(query):
    try:
        connection = psycopg2.connect(**conn_params)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    except Exception as error:
        print(f"Ошибка: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def insert(query):
    try:
        connection = psycopg2.connect(database="Barabulka", user="postgres", password="123123", host="localhost", port="5432")
        cursor = connection.cursor()
        cursor.execute(query=query)
        connection.commit()

    except Exception as error:
        print(f"Произошла ошибка: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()



