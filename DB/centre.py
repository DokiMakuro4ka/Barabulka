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
                    FROM Users
                    WHERE ID_user = {user_id}"""
        result = select(query=query)
        return result

    def insert_user(user_id, class_id):
        query = f"""INSERT INTO Users (ID_user, lvl, experience_now, experience_future, hp, damage, defence, agility, star_coin, ID_class, ID_subclass)
                    VALUES ({user_id}, 1, 0, 10, 10, 1, 1, 1, 0, {class_id}, 0)"""
        insert(query=query)


class Clas:
    def get_clas(clas_id):
        query = f"""SELECT *
                    FROM Classes
                    WHERE ID_class = {clas_id}"""
        result = select(query=query)
        return result


class Subclass:
    def get_subclass(subclass_id):
        query = f"""SELECT *
                    FROM Subclasses
                    WHERE ID_subclass = {subclass_id}"""
        result = select(query=query)
        return result


class Mob:
    pass



def select(query):
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
