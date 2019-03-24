from db_handler import connection_handler


@connection_handler(db_file='test_data/sqlite.db')
def db_function(connection, cursor):
    return {'connection': connection, 'cursor': cursor}


def test_create_connection_passes_connection_to_decorated_function():
    assert 'sqlite3.Connection' in str(db_function()['connection'])


def test_create_connection_passes_cursor_to_decorated_function():
    assert 'sqlite3.Cursor' in str(db_function()['cursor'])
