import unittest
from entities.budget import Budget
from entities.user import User
from service.budgetapp_service import BudgetappService

# User(username, password, balance,income, expenses)
# Budget(name, user, og_amount, c_amount, b_id)
# Purchase(category, amount, user, comment, p_id)


class TestBudgetappService(unittest.TestCase):
    def setUp(self):
        self.budget_service = BudgetappService()
        self.testuser = User('MrTest', 'test123', 1000.0, 500.0, 100.0)
        self.testbudget = Budget(1, 'MrTest', 'MayBudget', 300.0, 300.0)

    def test_create_user(self):
        self.budget_service.create_user(
            'MrTest', 'test123', 1000.0, 500.0, 100.0)
        self.assertNotEqual(self.budget_service._user, None)

    def test_create_budget(self):
        self.budget_service.create_budget('MrTest', 'MayBudget', 200.0)
        self.assertNotEqual(self.budget_service.budget, None)

    def test_add_purchase_removes_money_from_budget(self):
        self.budget_service.budget = self.testbudget
        self.budget_service.add_purchase(self.testbudget, 50, 'Food', '')
        self.assertEqual(str(self.budget_service.budget.left_amount), '250.0')
