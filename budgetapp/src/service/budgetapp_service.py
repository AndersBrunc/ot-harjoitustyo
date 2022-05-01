from entities.budget import Budget
from entities.user import User
from entities.purchase import Purchase

from databases.purchase_repository import (
    purchase_repository as default_purchase_repository
)
from databases.budget_repository import (
    budget_repository as default_budget_repository
)
from databases.users_repository import (
    user_repository as default_user_repository
)


class UsernameTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class NegativeInputError(Exception):
    pass


class BudgetappService:
    '''The class of the application service'''

    def __init__(
        self,
        purchase_repository=default_purchase_repository,
        budget_repository=default_budget_repository,
        user_repository=default_user_repository
    ):
        '''The constructor of the class, creates a new service session

        Args:
            purchase_repository:
                Optional, defaults to PurchaseRepository-object
                Object, that represents the purchase repository
            budget_repository:
                Optional, defaults to BudgetRepository-object
                Object, that represents the budget repository
            user_repository:
                Optional, defaults to UserRepository-object
                Object, that represents the user repository
        '''

        self._user = None
        self._purchase_repository = purchase_repository
        self._budget_repository = budget_repository
        self._user_repository = user_repository

    def create_budget(self, name, amount):
        '''Creates a budget

        Args:
            user: User-object, represents user
            name: string, represents name of budget
            amount: float, represents the original budget amount

        Returns:
            budget as Budget-object
        '''
        if amount < 0:
            raise NegativeInputError('The purchase amount must be positive')

        budget = Budget(name=name, username=self._user.username,
                        og_amount=amount, c_amount=amount)

        return self._budget_repository.add_budget(budget)

    def add_purchase(self, budget_id, amount, category, comment):
        '''Adds the users purchase to repository of purchases, and
           removes the receipt amount from the budget and balance of user

        Args:
            budget_id: Budget-id, represents the id of the budget that will be operated on
            amount: float, represents the receipt amount
            category: string, represents the purchased item(s) category
            comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase

        Returns:
            the addded purchase as Purchase-object

        '''

        if amount < 0:
            raise NegativeInputError('The purchase amount must be positive')

        purchase = Purchase(budget_id, category, amount,
                            self._user.username, comment)

        self._purchase_repository.add_purchase(purchase)

        self._user.balance -= amount
        self._user_repository.update_balance(
            self._user.balance, self._user.username)

        c_amount = self._budget_repository.find_by_id(budget_id).c_amount
        c_amount -= amount

        self._budget_repository.update_current_amount(c_amount, budget_id)

        return purchase

    def login(self, username, password):
        '''Logs user in

        Args:
            username: string, represents users username
            password: string, represents users password

        Returns:
            User as User-object

        Raises:
            InvalidCredentialsError:
                Error raised if entered username and password are falsely paired
        '''
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError(
                'Invalid username or password entered')

        self._user = user
        return user

    def create_user(self, username, password, balance, income, expenses, login=True):
        '''Creates a new user

        Args:

            username: string, represents the user's username
            password: string, represents the user's password
            balance: float , represents the users current balance
            income: float , represents the users current monthly income
            expenses: float , represents the users monthly recurring expenses

        Returns:
            user as User-object

        '''
        is_username_taken = self._user_repository.find_by_username(username)

        if is_username_taken:
            raise UsernameTakenError(f'The username {username} is taken')

        if balance < 0 or income < 0 or expenses < 0:
            raise NegativeInputError(
                'The balance, income and expenses need to be posistive numbers')

        user = self._user_repository.create_user(
            User(username, password, balance, income, expenses)
        )
        if login:
            self._user = user

        return user

    def current_user(self):
        '''Shows the current user

        Returns:
            User-object of current user
        '''
        return self._user

    def fetch_all_users(self):
        '''Returns all users in the user repository

        Returns:
            User-objects in a list

        '''
        return self._user_repository.fetch_all()

    def fetch_user_budgets(self):
        '''Returns all of the users budgets

        Returns:
            Budget-objects in a list
        '''
        return self._budget_repository.find_by_username(self._user.username)

    def fetch_user_purchases(self):
        '''Returns all of the users purchases

        Returns:
            Purchase-objects in a list
        '''

        return self._purchase_repository.find_by_username(self._user.username)

    def logout(self):
        '''Logs user out
        '''
        self._user = None

    def delete_purchase(self, purchase_id):
        '''Deletes specific purchase and "gives the money back" to the user

        Args:
            purchase_id: the id of the purchase

        '''
        purchase = self._purchase_repository.find_by_id(purchase_id)
        self._user.balance += purchase.amount
        try:
            budget = self._budget_repository.find_by_id(purchase.budget_id)
            budget.c_amount += purchase.amount
            self._budget_repository.update_current_amount(
                budget.c_amount, budget.id)
        except IndexError:
            IndexError('Budget does not excist')

        self._user_repository.update_balance(
            self._user.balance, self._user.username)
        self._purchase_repository.delete_one(purchase_id)

    def delete_budget(self, budget_id):
        '''Deletes specific budget

        Args:
            budget_id: the id of the budget

        '''
        self._budget_repository.delete_one(budget_id)

    def update_user_economy_value(self, value, new_amount):
        '''Updates the specified value to specified amount

        Args:
            value: string, the value to be updated
            new_amount: float, the new value
        '''

        if value == 'Balance':
            self._user.balance = new_amount
            self._user_repository.update_balance(
                new_amount, self._user.username)
        if value == 'Income':
            self._user.income = new_amount
            self._user_repository.update_income(
                new_amount, self._user.username)
        if value == 'Expenses':
            self._user.expenses = new_amount
            self._user_repository.update_expenses(
                new_amount, self._user.username)


budgetapp_service = BudgetappService()
