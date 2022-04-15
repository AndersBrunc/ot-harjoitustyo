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


class BudgetappService:
    '''The class of the application service'''

    def __init__(
        self,
        purchase_repository=default_purchase_repository,
        budget_repository=default_budget_repository,
        user_repository=default_user_repository
    ):
        '''The constructor of the class, creates a new service session'''

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
        budget = Budget(name=name, user=self._user,
                        og_amount=amount, c_amount=amount)

        return self._budget_repository.add_budget(budget)

    def create_user(self, username, password, balance, income, expenses):
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

        user = self._user_repository.create(
            User(username, password, balance, income, expenses)
        )
        if login:
            self._user = user

        return user

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
        '''
        purchase = self._purchase_repository.add_purchase(
            Purchase(category, amount, self._user, comment)
        )

        self._budget_repository.remove_amount(amount, budget_id)
        self._user.balance -= amount

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

        if user.password != password or not user:
            raise InvalidCredentialsError(
                'Invalid username or password entered')

        self._user = user
        return user

    def current_user(self):
        '''Shows the current user

        Returns:
            User-object of current user
        '''
        return self._user

    def logout(self):
        '''Logs user out
        '''
        self._user = None


budgetapp_service = BudgetappService()
