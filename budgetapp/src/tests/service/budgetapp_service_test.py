import unittest
from entities.budget import Budget
from entities.user import User
from entities.purchase import Purchase
from service.budgetapp_service import (
    BudgetappService,
    InvalidCredentialsError,
    UsernameTakenError,
    NegativeInputError
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

    def update_balance(self, new, username):
        for user in self.users:
            if user.username == username:
                user.balance = new
                break

    def update_income(self, new, username):
        for user in self.users:
            if user.username == username:
                user.income = new
                break

    def update_expenses(self, new, username):
        for user in self.users:
            if user.username == username:
                user.expenses = new
                break


class FakeBudgetRepository:
    def __init__(self, budgets=None):
        self.budgets = []

    def fetch_all(self):
        return self.budgets

    def find_by_username(self, username):
        user_budgets = filter(
            lambda budget: budget and budget.username == username, self.budgets
        )
        return list(user_budgets)

    def find_by_id(self, b_id):
        budgets = filter(
            lambda budget: budget and budget.id == b_id, self.budgets
        )
        return list(budgets)[0]

    def add_budget(self, budget):
        self.budgets.append(budget)
        return budget

    def delete_one(self, budget_id):
        without_id = filter(lambda budget: budget.id !=
                            budget_id, self.budgets)
        self.budgets = list(without_id)

    def delete_all(self):
        self.budgets = []

    def update_current_amount(self, new, budget_id):
        for budget in self.budgets:
            if budget.id == budget_id:
                budget.c_amount = new
                break


class FakePurchaseRepository:
    def __init__(self, purchases=None):
        self.purchases = []

    def fetch_all(self):
        return self.purchases

    def find_by_username(self, username):
        user_purchases = filter(
            lambda purchase: purchase and purchase.username == username,
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

    def find_by_id(self, p_id):
        specific = filter(lambda p: p and p.id == p_id, self.purchases)
        return list(specific)[0]

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
            FakePurchaseRepository(),
            FakeBudgetRepository(),
            FakeUserRepository()
        )
        self.user_testuser = User('Testuser', 'test123', 1000.0, 500.0, 200.0)
        self.budget_a = Budget(
            'Budget_A', self.user_testuser.username, 200.0, 200.0)
        self.budget_b = Budget(
            'Budget_B', self.user_testuser.username, 100.0, 100.0)
        self.purchase_a = Purchase(
            self.budget_a.id, 'Food', 10, self.user_testuser.username, '')
        self.purchase_b = Purchase(self.budget_a.id,
                                   'Food', 5.5, self.user_testuser.username, 'Lidl')
        self.purchase_c = Purchase(self.budget_b.id,
                                   'Misc', 88, self.user_testuser.username, 'random stuff')

    def login_user(self, user):
        self.budgetapp_service.create_user(
            user.username,
            user.password,
            user.balance,
            user.income,
            user.expenses
        )
    def test_logout(self):
        self.login_user(self.user_testuser)
        self.budgetapp_service.logout()
        self.assertEqual(self.budgetapp_service.current_user(),None)

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
        self.assertEqual(
            self.budgetapp_service.current_user().username, username)

    def test_create_user_fails_if_already_exist(self):
        username = self.user_testuser.username

        self.budgetapp_service.create_user(username, '1', 2, 3, 4)

        self.assertRaises(
            UsernameTakenError,
            lambda: self.budgetapp_service.create_user(username, '4', 3, 2, 1)
        )

    def test_update_values(self):
        self.login_user(self.user_testuser)
        current = self.budgetapp_service.current_user()
        new_balance = 2000
        new_income = 1000
        new_expenses = 500

        self.budgetapp_service.update_user_economy_value('Balance',new_balance)
        self.budgetapp_service.update_user_economy_value('Income',new_income)
        self.budgetapp_service.update_user_economy_value('Expenses',new_expenses)

        updated_user = self.budgetapp_service.fetch_all_users()[0]

        self.assertEqual(current.balance, new_balance)
        self.assertEqual(current.income, new_income)
        self.assertEqual(current.expenses, new_expenses)
        self.assertEqual(str(updated_user.balance),'2000')
        self.assertEqual(str(updated_user.income),'1000')
        self.assertEqual(str(updated_user.expenses),'500')
    
    def test_create_user_negative_values_raises_error(self):

        self.assertRaises(
            NegativeInputError,
            lambda: self.budgetapp_service.create_user('a','a',-1,1,1))
        self.assertRaises(
            NegativeInputError,
            lambda: self.budgetapp_service.create_user('a','a',1,-1,1))
        self.assertRaises(
            NegativeInputError,
            lambda: self.budgetapp_service.create_user('a','a',1,1,-1))
        
    def test_create_negative_budget_raises_error(self):
        self.login_user(self.user_testuser)
        self.assertRaises(
            NegativeInputError,
            lambda: self.budgetapp_service.create_budget('bad',-100)
        )
    
    def test_add_negative_purchase_raises_error(self):
        self.assertRaises(
            NegativeInputError,
            lambda: self.budgetapp_service.add_purchase('1',-123,'nope','')
        )

    def test_add_purchase_reduces_user_balance_and_budget(self):
        self.login_user(self.user_testuser)
        current = self.budgetapp_service.current_user()
        budget = self.budgetapp_service.create_budget(
            self.budget_a.name,
            self.budget_a.og_amount
        )
        purchase = self.purchase_a


        self.budgetapp_service.add_purchase(
            budget.id,
            purchase.amount,
            purchase.category,
            purchase.comment
        )

        updated_budget = self.budgetapp_service.fetch_user_budgets()[0]
        updated_user = self.budgetapp_service.fetch_all_users()[0]
        all_purchases = self.budgetapp_service.fetch_user_purchases()
        
        self.assertEqual(len(all_purchases),1)
        self.assertEqual(str(current.balance), '990.0')
        self.assertEqual(str(updated_user.balance),'990.0')
        self.assertEqual(str(updated_budget.c_amount),'190.0')


    def test_delete_purchase_updates_users_balance_and_budget_current_amount(self):
        self.login_user(self.user_testuser)
        current = self.budgetapp_service.current_user()

        budget = self.budgetapp_service.create_budget(
            self.budget_a.name,
            self.budget_a.og_amount
        )
        purchase = self.budgetapp_service.add_purchase(
            budget.id,
            self.purchase_a.amount,
            self.purchase_a.category,
            self.purchase_a.comment
        )

        self.budgetapp_service.delete_purchase(purchase.id)

        updated_budget = self.budgetapp_service.fetch_user_budgets()[0]
        updated_user = self.budgetapp_service.fetch_all_users()[0]

        self.assertEqual(str(current.balance), '1000.0')
        self.assertEqual(str(updated_user.balance),'1000.0')
        self.assertEqual(str(updated_budget.c_amount),'200.0')

