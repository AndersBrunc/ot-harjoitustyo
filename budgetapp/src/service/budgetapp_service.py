from entities.budget import Budget
from entities.user import User
from entities.purchase import Purchase


class BudgetappService:
    '''The class of the application service'''

    def __init__(self):
        '''The constructor of the class, creates a new service session'''

        self.user = None

    def create_budget(self, user, name, amount):
        '''Creates a budget

        Args:
            user: User-object, represents user
            name: string, represents name of budget
            amount: float, represents the original budget amount

        Returns:
            budget as Budget-object
        '''
        self.budget = Budget(user, name, amount)

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
        user = User(username, password, balance, income, expenses)
        self.user = user
        return user

    def add_purchase(self, budget, amount, category, comment):
        '''Adds the users purchase to repository of purchases, and
           removes the receipt amount from the budget

        Args:
            budget: Budget-object, represents the budget that will be operated on
            amout: float, represents the receipt amount
            category: string, represents the purchased item(s) category
            comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
        '''
        purchase = Purchase(amount, category, comment)

        self.budget.left_amount -= amount
