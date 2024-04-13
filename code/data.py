import sqlite3

from log import logger
from config import DB_NAME


def create_db():
    connection = sqlite3.connect(DB_NAME)
    connection.close()


def execute_query(query: str, data: tuple | None = None, db_name: str = DB_NAME):
    try:
        connection = sqlite3.connect(db_name, check_same_thread=False)
        cursor = connection.cursor()

        if data:
            cursor.execute(query, data)
            connection.commit()
        else:
            cursor.execute(query)

    except sqlite3.Error as e:
        error_msg = f"Ошибка: {e}"
        logger.error(error_msg)

    else:
        result = cursor.fetchall()
        connection.close()
        return result


def create_users_data_table():
    sql_query = (
        "CREATE TABLE IF NOT EXISTS users_data "
        "(id INTEGER PRIMARY KEY, "
        "user_id INTEGER, "
        "message TEXT, "
        "message_len INTEGER);"
    )
    execute_query(sql_query)


def add_new_message(text: str, user_id: int):
    message_len = len(text)
    sql_query = (
        'INSERT INTO user_data '
        '(user_id, message, message_len) '
        'VALUES (?, ?, ?);'
    )
    execute_query(sql_query, (user_id, text, message_len))


def is_user_in_table(user_id: int) -> bool:
    sql_query = (
        f'SELECT * '
        f'FROM users_data '
        f'WHERE user_id = ?;'
    )
    return bool(execute_query(sql_query, (user_id,)))


def check_len():
    sql_query = (
        'SELECT message_len '
        'FROM users_data;'
    )
    execute_query(sql_query)
    ''
    return


create_users_data_table()
