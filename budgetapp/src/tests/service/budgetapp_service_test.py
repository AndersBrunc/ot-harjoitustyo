import unittest
from entities.budget import Budget
from entities.user import User
from entities.purchase import Purchase
from service.budgetapp_service import (
    BudgetappService,
    InvalidCredentialsError,
    UsernameTakenError
)


class FakeUserRepository:
    def __init__(self, users=None):
        self.users = users or []

    def fetch_all(self):
        return self.users

    def create_user(self, user):
        self.users.append(user)
        return user

    def delete_all(self):
        self.users = []

    def find_by_username(self, username):
        matching_users = filter(
            lambda user: user.username == username, self.users)
        new_list = list(matching_users)
        return new_list[0] if len(new_list) > 0 else None


class FakeBudgetRepository:
    def __init__(self, budgets=None):
        self.budgets = []

    def fetch_all(self):
        return self.budgets

    def find_by_username(self, username):
        user_budgets = filter(
            lambda budget: budget.user and budget.user.username == username, self.budgets
        )
        return list(user_budgets)

    def create_budget(self, budget):
        self.budgets.append(budget)
        return budget

    def delete_one(self, budget_id):
        without_id = filter(lambda budget: budget.id !=
                            budget_id, self.budgets)
        self.budgets = list(without_id)

    def delete_all(self):
        self.budgets = []


class FakePurchaseRepository:
    def __init__(self, purchases=None):
        self.purchases = []

    def fetch_all(self):
        return self.purchases

    def find_by_username(self, username):
        user_purchases = filter(
            lambda purchase: purchase.user and purchase.user.username == username,
            self.purchases
        )
        return list(user_purchases)

    def find_by_category(self, username, category):
        user_purchases = self.find_by_username(username)
        categorized = filter(
            lambda purchase: purchase and purchase.category == category,
            user_purchases
        )

        return list(categorized)

    def add_purchase(self, purchase):
        self.purchases.append(purchase)
        return purchase

    def delete_one(self, purchase_id):
        without_id = filter(lambda purchase: purchase.id !=
                            purchase_id, self.purchases)
        self.purchases = list(without_id)

    def delete_all(self):
        self.purchases = []


class TestBudgetappService(unittest.TestCase):
    def setUp(self):
        self.budgetapp_service = BudgetappService(
            FakePurchaseRepository,
            FakeBudgetRepository(),
            FakeUserRepository()
        )
        self.user_testuser = User('Testuser', 'test123', 1000, 500, 200)
        self.budget_a = Budget('Budget_A', self.user_testuser.username, 200, 200)
        self.budget_b = Budget('Budget_A', self.user_testuser.username, 200, 200)
        self.purchase_a = Purchase('Food', 10, self.user_testuser.username, '')
        self.purchase_b = Purchase('Food', 5.5, self.user_testuser.username, 'Lidl')
        self.purchase_c = Purchase(
            'Misc', 88, self.user_testuser.username, 'random stuff')

    def login_user(self, user):
        self.budgetapp_service.create_user(
            user.username,
            user.password,
            user.balance,
            user.income,
            user.expenses
        )

    def test_login_success_with_correct_credentials(self):
        self.budgetapp_service.create_user(
            self.user_testuser.username,
            self.user_testuser.password,
            self.user_testuser.balance,
            self.user_testuser.income,
            self.user_testuser.expenses
        )

        user = self.budgetapp_service.login(
            self.user_testuser.username,
            self.user_testuser.password
        )
        self.assertEqual(user.username, self.user_testuser.username)

    def test_login_fails_with_wrong_credentials(self):
        self.assertRaises(
            InvalidCredentialsError,
            lambda: self.budgetapp_service.login('wrong', 'credentials')
        )

    def test_get_current_user(self):
        self.login_user(self.user_testuser)

        current = self.budgetapp_service.current_user()

        self.assertEqual(current.username, self.user_testuser.username)

    def test_create_new_non_existing_user(self):
        username = self.user_testuser.username
        password = self.user_testuser.password
        balance = self.user_testuser.balance
        income = self.user_testuser.income
        expenses = self.user_testuser.expenses

        self.budgetapp_service.create_user(
            username,
            password,
            balance,
            income,
            expenses
        )
        all_users = self.budgetapp_service.fetch_all_users()

        self.assertEqual(len(all_users), 1)
        self.assertEqual(all_users[0].username, username)

    def test_create_user_fails_if_already_exist(self):
        username = self.user_testuser.username

        self.budgetapp_service.create_user(username, '1', 2, 3, 4)

        self.assertRaises(
            UsernameTakenError,
            lambda: self.budgetapp_service.create_user(username, '4', 3, 2, 1)
        )
