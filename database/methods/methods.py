import sqlite3
from typing import List, Optional, Tuple

DB_NAME = 'database/schedule_bot.db'

# Управление подключением к базе данных с помощью контекстного менеджера
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Чтобы результат запроса был в виде словаря
    return conn

# Регистрация пользователя в базе данных
def register_user(telegram_id: int, first_name: str) -> None:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (telegram_id, first_name)
            VALUES (?, ?)
        ''', (telegram_id, first_name))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error while registering user: {e}")
    finally:
        conn.close()

# Получение расписания по группе и дню недели
def get_group_schedule(group_name: str, day_of_week: Optional[int] = None) -> List[Tuple]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if day_of_week:
            cursor.execute('''
                SELECT * FROM schedule
                WHERE group_name = ? AND day_of_week_int = ?
            ''', (group_name, day_of_week))  # Используем числовое значение дня недели
        else:
            cursor.execute('''
                SELECT * FROM schedule
                WHERE group_name = ?
            ''', (group_name,))

        schedule = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error while fetching schedule: {e}")
        schedule = []
    finally:
        conn.close()

    return schedule



# Получение списка групп для клавиатуры
def get_groups() -> List[str]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT group_name FROM schedule')
        groups = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error while fetching groups: {e}")
        groups = []
    finally:
        conn.close()

    return [group['group_name'] for group in groups]

def get_all_users() -> list[dict]:
    """
    Получает список всех пользователей из базы данных.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT telegram_id, first_name FROM users')
        users = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error while fetching users: {e}")
        users = []
    finally:
        conn.close()

    return [{"id_telegram": user["telegram_id"], "username": user["first_name"]} for user in users]

