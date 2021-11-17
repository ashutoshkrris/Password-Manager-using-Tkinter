import sqlite3


def init_database():
    with sqlite3.connect("password_vault.db") as db:
        cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS master(
            id INTEGER PRIMARY KEY,
            password TEXT NOT NULL);
            """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault(
            id INTEGER PRIMARY KEY,
            platform TEXT NOT NULL,
            userid TEXT NOT NULL,
            password TEXT NOT NULL);
            """)
    return db, cursor
