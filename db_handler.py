import sqlite3
from functools import wraps
from sqlite3 import Error
from config import DB_FILE


def connection_handler(db_file=DB_FILE):
    """Open & close SQLite database connection for decorated function, unless caller has passed one already"""
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if any('sqlite3' in str(type(arg)) for arg in args):
                print('condition matched')
                return fn(*args, **kwargs)
            else:
                try:
                    connection = sqlite3.connect(db_file)
                    cursor = connection.cursor()
                    result = fn(connection, cursor, *args, **kwargs)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    return result
                except Error as err:
                    print(err)
                finally:
                    connection.close()
        return wrapper
    return inner
