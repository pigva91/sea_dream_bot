import sqlite3

db = sqlite3.connect('users.db', check_same_thread=False)
cur = db.cursor()


def create_table():
    """Создает таблицу users в базе данных, если она еще не существует."""
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        users_id INTEGER)
    ''')
    db.commit()



def check_id(id):
    """Проверяет, существует ли пользователь с указанным ID в базе данных."""
    check_value = id
    cur.execute(
        '''SELECT COUNT(*) FROM users WHERE users_id = ?''',
        (check_value, )
    )
    count = cur.fetchone()[0]
    return count


def insert_id(id):
    """Добавляет новый идентификатор пользователя в таблицу users."""
    user_id = id
    cur.execute(
        '''INSERT INTO users (users_id) VALUES (?)''',
        (user_id, )
    )
    db.commit()






