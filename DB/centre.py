import psycopg2


# Параметры подключения
conn_params = {
    "dbname": "Barabulka",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}


class User:
    def get_user(user_id):
        query = f"""SELECT *
                    FROM "Users"
                    WHERE user_id = {user_id}"""
        result = select_update(query=query)
        return result

    def set_user_name(user_id, name):
        query = f"""UPDATE "Users"
                    SET name = '{name}'
                    WHERE user_id = {user_id}"""
        select_update(query=query)

    def set_user_lvl(user_id, lvl):
        pass

    def set_user_experience_now(user_id, experience_now):
        pass

    def set_user_experience_future(user_id, experience_future):
        pass

    def set_user_hp(user_id, hp):
        pass

    def set_user_damage(user_id, damage):
        pass

    def set_user_defence(user_id, defence):
        pass

    def set_user_agility(user_id, agility):
        pass

    def set_user_star_coin(user_id, star_coin):
        pass

    def set_user_skill_point(user_id, skill_coin):
        pass

    def insert_user(user_id, class_id):
        query = f"""INSERT INTO "Users" (user_id, name, lvl, experience_now, experience_future, hp, damage, defence, agility, star_coin, skill_point, class_id, subclass_id, state_id)
                    VALUES ({user_id}, 'f', 1, 0, 10, 10, 1, 1, 1, 0, 0, {class_id}, 0, 0)"""
        insert(query=query)


class UserClass:
    def get_class(class_id):
        query = f"""SELECT *
                    FROM "Classes"
                    WHERE class_id = {class_id}"""
        result = select_update(query=query)
        return result


class UserSubclass:
    def get_subclass(subclass_id):
        query = f"""SELECT *
                    FROM "Subclasses"
                    WHERE subclass_id = {subclass_id}"""
        result = select_update(query=query)
        return result


class Mob:
    pass



def select_update(query):
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
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
        if conn is not None:
            conn.close()

def insert(query):
    try:
        connection = psycopg2.connect(database="Barabulka", user="postgres", password="admin", host="localhost", port="5432")
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



