from db_connection import get_database_connection


def drop_tables(connection):

    cursor = connection.cursor()
    cursor.execute('''drop table if exists users;''')
    cursor.execute('''drop table if exists budgets;''')
    cursor.execute('''drop table if exists purchases;''')
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
            username text,
            og_amount float,
            c_amount float,
            b_id text
        );
    ''')
    cursor.execute('''
        create table purchases (
            p_id text primary key,
            category text,
            amount float,
            username text,
            comment text,
            budget_id text
        );
    ''')

    connection.commit()


def initialize_db():

    connection = get_database_connection()

    drop_tables(connection)

    create_tables(connection)


if __name__ == '__main__':
    initialize_db()
