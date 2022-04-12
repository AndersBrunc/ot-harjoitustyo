from pathlib import Path
from entities.budget import Budget
from config import BUDGET_FILE_PATH


class BudgetRepository:
    '''Class of the purchases
    '''

    def __init__(self, path):
        '''Class constructor
            Args:
            path: path to the location for saving the budgets
        '''
        self._path = path

    def _check_file_exists(self):
        Path(self._path).touch()

    def _write(self, budgets):
        self._check_file_exists()

        with open(self._path, 'w', encoding='utf-8') as file:
            for budget in budgets:
                row = f'{budget.id}{budget.user};{budget.name};{budget.og_amount};{budget.c_amount}'
                file.write(row+'\n')

    def _read(self):
        budgets = []
        self._check_file_exists()

        with open(self._path, encoding='utf-8') as file:
            for row in file:
                row = row.replace('\n', '')
                row_piece = row.split(';')

                b_id = row_piece[0]
                user = row_piece[1]
                name = row_piece[2]
                og_amount = row_piece[3]
                left_amount = row_piece[4]

                budgets.append(
                    Budget(user, name, og_amount, left_amount, b_id))

            return budgets

    def fetch_all(self):
        '''Returns all budgets
        Returns:
            list of Budget-objects
        '''
        return self._read()

    def add_budget(self, budget):
        '''Saves a budget in the budget-database
        Args:
            budget: Budget-object that will be saved

        '''
        all_budgets = self.fetch_all()
        all_budgets.append(budget)
        self._write(all_budgets)

        return True

    def delete_one(self, p_id):
        '''Deletes specific budget

        Args:
            b_id: id of the deleted budget

        '''
        self._check_file_exists()
        all_budgets = self.fetch_all()
        edited_list = filter(lambda budget: budget.id != p_id, all_budgets)
        self._write(edited_list)

    def delete_all(self):
        '''Deletes all budgets
        '''
        self._write([])

budget_repository = BudgetRepository(BUDGET_FILE_PATH)
