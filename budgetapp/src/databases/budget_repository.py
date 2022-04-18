from entities.budget import Budget
from db_connection import get_database_connection


def get_budget_by_row(row):
    return Budget(row['name'], row['username'], row['og_amount'], row['c_amount']) if row else None


class BudgetRepository:
    '''Class of the budget-repository
    '''

    def __init__(self, connection):
        '''class constructor

        Args:
            connection: database connection object

        '''
        self._connection = connection

    def add_budget(self, budget):
        '''Adds budget to the database

        Args:
            budget: the budget to be added

        Returns:
            The added budget as Budget-object

        '''

        cursor = self._connection.cursor()
        cursor.execute(
            'insert into budgets (name,username,og_amount,c_amount,b_id) values (?,?,?,?,?)',
            (budget.name, budget.username,
             budget.og_amount, budget.c_amount, budget.id)
        )
        self._connection.commit()

        return budget

    def fetch_all(self):
        '''Returns all budgets
        Returns:
            list of Budget-objects
        '''

        cursor = self._connection.cursor()
        cursor.execute('select * from budgets')
        rows = cursor.fetchall()

        return list(map(get_budget_by_row, rows))

    def find_by_username(self, username):
        '''Finds budget based on username

        Args:
            username: the username the search is based on

        Returns:
            The list of budgets as Budget-objects if in existance, otherwhise None

        '''
        all_budgets = self.fetch_all()
        new = filter(lambda budget: budget.username == username, all_budgets)
        return list(new)

    def find_by_id(self, b_id):
        '''Finds budget based on it's id
        Args:
            b_id: the budget-id the search is based on

        Returns:
            The Budget-object if in existance, otherwhise None

        '''
        cursor = self._connection.cursor()
        cursor.execute('select * from budgets where b_id = ?',(b_id,))
        rows = cursor.fetchall()

        return list(map(get_budget_by_row, rows))[0]

    def delete_one(self, b_id):
        '''Deletes specific budget

        Args:
            b_id: id of the deleted budget

        '''
        cursor = self._connection.cursor()
        cursor.execute('delete from budgets where b_id = ?', (b_id,))
        self._connection.commit()

    def delete_all(self):
        '''Deletes all budgets
        '''
        cursor = self._connection.cursor()
        cursor.execute('delete from budgets')
        self._connection.commit()

    def update_current_amount(self, new, b_id):
        '''Updates the budgets current amount

        Args:
            new: the new amount
            b_id: id of the budget
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            'update budgets set c_amount = ? where b_id = ?', (new, b_id))
        self._connection.commit()


budget_repository = BudgetRepository(get_database_connection())
