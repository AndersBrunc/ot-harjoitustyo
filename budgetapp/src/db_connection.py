import os
import sqlite3

directory = os.path.dirname(__file__)

connect = sqlite3.connect(os.path.join(
    directory, '..', 'data', 'database.sqlite'))
connect.row_factory = sqlite3.Row


def get_database_connection():
    return connect
