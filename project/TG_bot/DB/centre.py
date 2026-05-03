import psycopg2
from config.settings import Config

def get_connection():
    return psycopg2.connect(Config.db_dsn())

class State:
    @staticmethod
    def get_state(state_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "States" WHERE state_id = %s', (state_id,))
                return cur.fetchone()
    @staticmethod
    def get_state_by_name(name):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "States" WHERE name = %s', (name,))
                return cur.fetchone()

class Epoch:
    @staticmethod
    def get_epoch_by_name(name):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "Epochs" WHERE name = %s', (name,))
                return cur.fetchone()
    @staticmethod
    def get_epochs_by_state(state_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "Epochs" WHERE state_id = %s ORDER BY epoch_id', (state_id,))
                return cur.fetchall()

class EpochDetail:
    @staticmethod
    def get_details_by_epoch(epoch_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "EpochDetails" WHERE epoch_id = %s', (epoch_id,))
                return cur.fetchall()
    @staticmethod
    def get_detail_by_category(epoch_id, category):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "EpochDetails" WHERE epoch_id = %s AND category = %s', (epoch_id, category))
                return cur.fetchone()

class User:
    @staticmethod
    def get_user(telegram_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "Users" WHERE telegram_id = %s', (telegram_id,))
                return cur.fetchone()
    @staticmethod
    def insert_user(telegram_id, name=None, state_id=1, class_id=1, subclass_id=1, location_id=1):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO "Users" (telegram_id, name, state_id, class_id, subclass_id, location_id, hp, max_hp, mana, max_mana, damage, defence) '
                    'VALUES (%s, %s, %s, %s, %s, %s, 100, 100, 50, 50, 15, 5) ON CONFLICT (telegram_id) DO NOTHING',
                    (telegram_id, name or "Странник", state_id, class_id, subclass_id, location_id)
                )
                conn.commit()
    @staticmethod
    def set_field(telegram_id, field, value):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f'UPDATE "Users" SET {field} = %s WHERE telegram_id = %s', (value, telegram_id))
                conn.commit()
    @staticmethod
    def delete_user(telegram_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM "Battles" WHERE user_id = (SELECT user_id FROM "Users" WHERE telegram_id = %s)', (telegram_id,))
                cur.execute('DELETE FROM "ActiveQuests" WHERE user_id = (SELECT user_id FROM "Users" WHERE telegram_id = %s)', (telegram_id,))
                cur.execute('DELETE FROM "Inventory" WHERE user_id = (SELECT user_id FROM "Users" WHERE telegram_id = %s)', (telegram_id,))
                cur.execute('DELETE FROM "Users" WHERE telegram_id = %s', (telegram_id,))
                conn.commit()
    @staticmethod
    def get_user_text(telegram_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT name, lvl, experience_now, experience_future, hp, max_hp, mana, max_mana, damage, defence, star_coin, class_id, subclass_id FROM "Users" WHERE telegram_id = %s', (telegram_id,))
                row = cur.fetchone()
                if row:
                    name, lvl, exp_now, exp_future, hp, max_hp, mana, max_mana, dmg, defence, coins, class_id, subclass_id = row
                    class_name = "Не выбран"
                    if class_id:
                        cls = UserClass.get_class(class_id)
                        if cls:
                            class_name = cls[2]  # имя класса на индексе 2
                    subclass_name = ""
                    if subclass_id and subclass_id != 0:
                        sub = UserSubclass.get_subclass(subclass_id)
                        if sub:
                            subclass_name = f"\n✨ Подкласс: {sub[2]}"
                    return (f"👤 {name} (уровень {lvl})\n"
                            f"📖 Класс: {class_name}{subclass_name}\n"
                            f"❤️ {hp}/{max_hp} HP\n"
                            f"🔮 {mana}/{max_mana} MP\n"
                            f"⚔️ Атака: {dmg}  🛡 Защита: {defence}\n"
                            f"✨ Опыт: {exp_now}/{exp_future}\n"
                            f"💰 Монет: {coins}")
                return "Профиль не найден"

class UserClass:
    @staticmethod
    def get_class(class_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "Classes" WHERE class_id = %s', (class_id,))
                return cur.fetchone()

class UserSubclass:
    @staticmethod
    def get_subclass(subclass_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "Subclasses" WHERE subclass_id = %s', (subclass_id,))
                return cur.fetchone()

class Monster:
    @staticmethod
    def get_random_monster_by_location(location_id, player_level=1):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "Monsters" WHERE location_id = %s AND level <= %s ORDER BY random() LIMIT 1', (location_id, player_level+2))
                monster = cur.fetchone()
                if not monster:
                    cur.execute('SELECT * FROM "Monsters" ORDER BY random() LIMIT 1')
                    monster = cur.fetchone()
                return monster

class BattleLog:
    @staticmethod
    def save_battle(telegram_id, monster_id, result, exp_gained, star_coin_gained, log_text=""):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT user_id FROM "Users" WHERE telegram_id = %s', (telegram_id,))
                user_row = cur.fetchone()
                if user_row:
                    user_id = user_row[0]
                    cur.execute(
                        'INSERT INTO "Battles" (user_id, monster_id, battle_type, result, experience_gained, star_coin_gained, battle_log) '
                        'VALUES (%s, %s, \'pve\', %s, %s, %s, %s)',
                        (user_id, monster_id, result, exp_gained, star_coin_gained, log_text)
                    )
                    conn.commit()