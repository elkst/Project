import sqlite3

def create_db():
    # Создание базы данных и таблиц
    conn = sqlite3.connect('database/schedule_bot.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE NOT NULL,
        first_name TEXT NOT NULL
    )''')

    # Таблица расписаний
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL,
        day_of_week TEXT NOT NULL,
        subject TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        teacher TEXT NOT NULL,
        building TEXT NOT NULL,
        room TEXT NOT NULL
    )''')

    conn.commit()
    conn.close()

# Создаём базу данных
create_db()

