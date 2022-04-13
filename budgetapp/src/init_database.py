from db_connection import get_database_connection

def drop_tables(connection):

    cursor = connection.cursor()
    cursor.execute('''drop table if exists budgets;''')
    connection.commit()

def create_tables(connection):

    cursor = connection.cursor()
    cursor.execute('''
        create table users (
            username text primary key,
            password text,
            balance float,
            income float,
            expenses float
        );
    ''')
    cursor.execute('''
        create table budgets (
            name text primary key,
            user text,
            original_amount float,
            current_amount float
        );
    ''')

    connection.commit()

def initialize_db():

    connection = get_database_connection()

    drop_tables(connection)

    create_tables(connection)

if __name__ =='__main__':
    initialize_db()
