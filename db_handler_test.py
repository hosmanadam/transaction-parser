import sqlite3

from config import TEST_DB_FILE
from db_handler import connection_handler


@connection_handler(db_file=TEST_DB_FILE)
def db_tester_function(connection, cursor):
    return {'connection': connection, 'cursor': cursor}


def test_connection_handler_passes_connection_to_decorated_function():
    assert 'sqlite3.Connection' in str(db_tester_function()['connection'])


def test_connection_handler_passes_cursor_to_decorated_function():
    assert 'sqlite3.Cursor' in str(db_tester_function()['cursor'])


def test_connection_handler_breaks_out_when_receiving_connection_and_cursor():
    connection = sqlite3.connect(TEST_DB_FILE)
    cursor = connection.cursor()
    assert db_tester_function(connection, cursor)['connection'] is connection
    assert db_tester_function(connection, cursor)['cursor'] is cursor
