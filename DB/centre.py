import os
import psycopg2


conn_params = {
    "dbname": os.getenv("DB_NAME", "Barabulka"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "123123"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def execute(query, params=None, fetch=False):
    try:
        with psycopg2.connect(**conn_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    result = [dict(zip(columns, row)) for row in rows]
                    return result
                connection.commit()
    except Exception as error:
        print(f"Ошибка: {error}")
        return None


# ------------------ Users ------------------
class User:
    @staticmethod
    def get_user(user_id):
        query = 'SELECT * FROM "Users" WHERE user_id = %s'
        result = execute(query, (user_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_user_text(user_id):
        user = User.get_user(user_id)
        if not user:
            return "Пользователь не найден."

        user_class = UserClass.get_class(user["class_id"])
        user_subclass = UserSubclass.get_subclass(user["subclass_id"])
        user_state = UserState.get_state(user["state_id"])

        class_name = user_class["name"] if user_class else "Не выбран"
        subclass_name = user_subclass["name"] if user_subclass else "Не выбран"
        state_name = user_state["name"] if user_state else "Неизвестно"

        return (
            f"Профиль (id {user['user_id']})\n"
            f"Имя: {user['name']}\n"
            f"Государство: {state_name}\n\n"
            f"Уровень: {user['lvl']}\n"
            f"Опыт: {user['experience_now']} / {user['experience_future']}\n\n"
            f"Класс: {class_name}\n"
            f"Подкласс: {subclass_name}\n\n"
            f"Здоровье: {user['hp']}\n"
            f"Урон: {user['damage']}\n"
            f"Защита: {user['defence']}\n"
            f"Ловкость: {user['agility']}\n"
            f"Очки навыков: {user['skill_point']}\n"
            f"Star Коины: {user['star_coin']}"
        )

    @staticmethod
    def set_field(user_id, field, value):
        query = f'UPDATE "Users" SET {field} = %s WHERE user_id = %s'
        execute(query, (value, user_id))

    @staticmethod
    def insert_user(user_id, state_id):
        query = """
            INSERT INTO "Users"
            (user_id, name, lvl, experience_now, experience_future, hp, damage, defence,
             agility, star_coin, skill_point, class_id, subclass_id, state_id)
            VALUES (%s, %s, 1, 0, 10, 10, 1, 1, 1, 0, 0, 0, 0, %s)
        """
        execute(query, (user_id, "0", state_id))

    @staticmethod
    def delete_user(user_id):
        query = 'DELETE FROM "Users" WHERE user_id = %s'
        execute(query, (user_id,))


# ------------------ Classes ------------------
class UserClass:
    @staticmethod
    def get_class(class_id):
        query = 'SELECT * FROM "Classes" WHERE class_id = %s'
        result = execute(query, (class_id,), fetch=True)
        return result[0] if result else None


# ------------------ Subclasses ------------------
class UserSubclass:
    @staticmethod
    def get_subclass(subclass_id):
        query = 'SELECT * FROM "Subclasses" WHERE subclass_id = %s'
        result = execute(query, (subclass_id,), fetch=True)
        return result[0] if result else None


# ------------------ States ------------------
class UserState:
    @staticmethod
    def get_state(state_id):
        query = 'SELECT * FROM "States" WHERE state_id = %s'
        result = execute(query, (state_id,), fetch=True)
        return result[0] if result else None


class State:
    @staticmethod
    def get_state(state_id):
        query = 'SELECT * FROM "States" WHERE state_id = %s'
        result = execute(query, (state_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_state_by_name(name):
        query = 'SELECT * FROM "States" WHERE name = %s'
        result = execute(query, (name,), fetch=True)
        return result[0] if result else None


# ------------------ Epochs ------------------
class Epoch:
    @staticmethod
    def get_epoch(epoch_id):
        query = 'SELECT * FROM "Epochs" WHERE epoch_id = %s'
        result = execute(query, (epoch_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_epoch_by_name(name):
        query = 'SELECT * FROM "Epochs" WHERE name = %s'
        result = execute(query, (name,), fetch=True)
        return result[0] if result else None


# ------------------ EpochDetails ------------------
class EpochDetail:
    @staticmethod
    def get_details(epoch_id):
        query = 'SELECT * FROM "EpochDetails" WHERE epoch_id = %s'
        result = execute(query, (epoch_id,), fetch=True)
        return result if result else None

    @staticmethod
    def get_detail_by_category(epoch_id, category):
        query = 'SELECT * FROM "EpochDetails" WHERE epoch_id = %s AND category = %s'
        result = execute(query, (epoch_id, category), fetch=True)
        return result[0] if result else None


# ------------------ Mob ------------------
class Mob:
    pass