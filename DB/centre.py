import psycopg2

# Параметры подключения
conn_params = {
    "dbname": "Barabulka",
    "user": "postgres",
    "password": "123123",
    "host": "localhost",
    "port": "5432"
}


def execute(query, fetch=False):
    """Универсальная функция для SELECT/UPDATE/INSERT"""
    try:
        with psycopg2.connect(**conn_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
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
        query = f'SELECT * FROM "Users" WHERE user_id = {user_id}'
        result = execute(query, fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_user_text(user_id):
        user = User.get_user(user_id)
        if not user:
            return "Пользователь не найден."

        user_class = UserClass.get_class(user["class_id"])
        user_subclass = UserSubclass.get_subclass(user["subclass_id"])
        user_state = UserState.get_state(user["state_id"])

        return (
            f"Профиль (id {user['user_id']})\n"
            f"Имя: {user['name']}\n"
            f"Государство: {user_state['name']}\n\n"
            f"Уровень: {user['lvl']}\n"
            f"Опыт: {user['experience_now']} / {user['experience_future']}\n\n"
            f"Класс: {user_class['name']}\n"
            f"Подкласс: {user_subclass['name']}\n\n"
            f"Здоровье: {user['hp']}\n"
            f"Урон: {user['damage']}\n"
            f"Защита: {user['defence']}\n"
            f"Ловкость: {user['agility']}\n"
            f"Очки навыков: {user['skill_point']}\n"
            f"Star Коины: {user['star_coin']}"
        )

    @staticmethod
    def set_field(user_id, field, value):
        query = f'UPDATE "Users" SET {field} = \'{value}\' WHERE user_id = {user_id}'
        execute(query)

    @staticmethod
    def insert_user(user_id, state_id):
        query = f"""INSERT INTO "Users" 
        (user_id, name, lvl, experience_now, experience_future, hp, damage, defence, agility, star_coin, skill_point, class_id, subclass_id, state_id)
        VALUES ({user_id}, '0', 1, 0, 10, 10, 1, 1, 1, 0, 0, 0, 0, {state_id})"""
        execute(query)


# ------------------ Classes ------------------
class UserClass:
    @staticmethod
    def get_class(class_id):
        query = f'SELECT * FROM "Classes" WHERE class_id = {class_id}'
        result = execute(query, fetch=True)
        return result[0] if result else None


# ------------------ Subclasses ------------------
class UserSubclass:
    @staticmethod
    def get_subclass(subclass_id):
        query = f'SELECT * FROM "Subclasses" WHERE subclass_id = {subclass_id}'
        result = execute(query, fetch=True)
        return result[0] if result else None


# ------------------ States ------------------
class UserState:
    @staticmethod
    def get_state(state_id):
        query = f'SELECT * FROM "States" WHERE state_id = {state_id}'
        result = execute(query, fetch=True)
        return result[0] if result else None


class State:
    @staticmethod
    def get_state(state_id):
        query = f'SELECT * FROM "States" WHERE state_id = {state_id}'
        result = execute(query, fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_state_by_name(name):
        query = f'SELECT * FROM "States" WHERE name = \'{name}\''
        result = execute(query, fetch=True)
        return result[0] if result else None


# ------------------ Epochs ------------------
class Epoch:
    @staticmethod
    def get_epoch(epoch_id):
        query = f'SELECT * FROM "Epochs" WHERE epoch_id = {epoch_id}'
        result = execute(query, fetch=True)
        return result[0] if result else None

    @staticmethod
    def get_epoch_by_name(name):
        query = f'SELECT * FROM "Epochs" WHERE name = \'{name}\''
        result = execute(query, fetch=True)
        return result[0] if result else None


# ------------------ EpochDetails ------------------
class EpochDetail:
    @staticmethod
    def get_details(epoch_id):
        query = f'SELECT * FROM "EpochDetails" WHERE epoch_id = {epoch_id}'
        result = execute(query, fetch=True)
        return result if result else None

    @staticmethod
    def get_detail_by_category(epoch_id, category):
        query = f'SELECT * FROM "EpochDetails" WHERE epoch_id = {epoch_id} AND category = \'{category}\''
        result = execute(query, fetch=True)
        return result[0] if result else None


# ------------------ Mob ------------------
class Mob:
    pass
