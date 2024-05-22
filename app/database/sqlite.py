import os
import sqlite3

from app.config import SQLITE_DB_PATH
from app.logger import get_logger


def get_sqlite_connection():
    return sqlite3.connect(SQLITE_DB_PATH)


def initialize_relation():
    logger = get_logger()
    file_exists = os.path.exists(SQLITE_DB_PATH)

    if file_exists:
        logger.info(f"The SQLite database file already exists.")
        return

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_relations (
        parent_id INTEGER,
        child_id INTEGER
    )
    ''')

    sql_insert = "INSERT INTO product_relations (parent_id, child_id) VALUES (?, ?)"
    data_to_insert = [
        (12, 13),
        (13, 14)
    ]
    # mock relations data
    cursor.executemany(sql_insert, data_to_insert)

    conn.commit()
    conn.close()
    logger.info("The SQLite database has been initialized.")


# Fetching relations data from SQLite DB
def get_relation() -> list:
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM product_relations")
    relations = cursor.fetchall()
    conn.close()
    return relations
