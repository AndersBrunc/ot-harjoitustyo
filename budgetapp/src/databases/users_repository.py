from entities.user import User
from db_connection import get_database_connection


def get_user_by_row(row):
    return User(row['username'], row['password'], row['balance'], row['income'], row['expenses']) if row else None


class UserRepository:
    '''The class of the user-database
    '''

    def __init__(self, connection):
        '''class constructor

        Args:
            connection: database connection object

        '''
        self._connection = connection

    def create_user(self, user):
        '''Adds user to the database

        Args:
            user: the user to be added

        Returns:
            The added user as User object

        '''
        cursor = self._connection.cursor()
        cursor.execute(
            'insert into users (username,password,balance,income,expenses) values (?,?,?,?,?)',
            (user.username, user.password, user.balance, user.income, user.expenses)
        )
        self._connection.commit()

    def fetch_all(self):
        '''Returns all users

        Returns: list of all users

        '''

        cursor = self._connection.cursor()
        cursor.execute('select * from users')
        rows = cursor.fetchall()

        return list(map(get_user_by_row, rows))

    def find_by_username(self, username):
        '''Finds user based on username

        Args:
            username: the username the search is based on

        Returns:
            The user as User-object if in existance, otherwhise None

        '''
        cursor = self._connection.cursor()
        cursor.execute(
            'select * from users where username = ?',
            (username,)
        )
        row = cursor.fetchone()

        return get_user_by_row(row)

    def delete_all(self):
        '''Deletes all users
        '''
        cursor = self._connection.cursor()
        cursor.execute('delete from users')
        self._connection.commit()
    
    def update_balance(self,new,username):
        '''Updates users balance

        Args:
            new: represents the new balance
            username: represents the users username

        '''
        cursor = self._connection.cursor()
        cursor.execute('update users set balance = ? where username = ?', (new,username,))
        self._connection.commit()

    def update_income(self,new,username):
        '''Updates users income
        
        Args:
            new: represents the new income
            username: represents the users username

        '''
        cursor = self._connection.cursor()
        cursor.execute('update users set income = ? where username = ?', (new,username,))
        self._connection.commit()

    def update_expenses(self,new,username):
        '''Updates users expenses

        Args:
            new: represents the new expenses
            username: represents the users username

        '''
        cursor = self._connection.cursor()
        cursor.execute('update users set expenses = ? where username = ?', (new,username,))
        self._connection.commit()



user_repository = UserRepository(get_database_connection())
