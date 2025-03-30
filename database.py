import sqlite3

# Функція для створення таблиці користувачів
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Додавання нового користувача
def add_user(user_id, first_name, last_name, username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, first_name, last_name, username)
        VALUES (?, ?, ?, ?)
    ''', (user_id, first_name, last_name, username))
    conn.commit()
    conn.close()

# Отримання всіх користувачів
def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Ініціалізація БД при першому запуску
init_db()
