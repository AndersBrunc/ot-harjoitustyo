import unittest
from databases.budget_repository import budget_repository
from entities.budget import Budget
from entities.budget import User

class TestBudgetRepository(unittest.Testcase):
    def setUp(self):
        budget_repository.delete_all()

        self.user = User('MrTest', 'test123')
        self.budget_a = Budget('Testbudget_A')
        self.budget_b = Budget('Testbudget_B')
        
    def test_create(self):
        budget_repository.add_budget(self.budget_a)
        budgets=budget_repository.fetch_all()

        assertEqual(len(budgets),1)
        assertEqual(budgets[0].name, self.budget_a.name)
        