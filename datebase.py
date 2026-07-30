import sqlite3


DB = "users.db"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        name TEXT,
        username TEXT,
        rating INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def save_user(telegram_id, name, username):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (telegram_id, name, username)
    VALUES (?, ?, ?)
    """,
    (
        telegram_id,
        name,
        username
    ))

    conn.commit()
    conn.close()


def save_rating(telegram_id, rating):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET rating = ?
    WHERE telegram_id = ?
    """,
    (
        rating,
        telegram_id
    ))

    conn.commit()
    conn.close()


def get_users_by_rating(rating):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT telegram_id FROM users WHERE rating=?",
        (rating,)
    )

    users = cursor.fetchall()

    conn.close()

    return [u[0] for u in users]


def get_all_users():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT telegram_id FROM users"
    )

    users = cursor.fetchall()

    conn.close()

    return [u[0] for u in users]
