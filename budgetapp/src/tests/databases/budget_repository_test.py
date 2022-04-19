import unittest
from databases.budget_repository import budget_repository
from entities.budget import Budget
from entities.user import User


class TestBudgetRepository(unittest.TestCase):
    def setUp(self):
        budget_repository.delete_all()
        self.user_mrtest = User('MrTest', 'test123', 1000, 500, 200)
        self.budget_a = Budget('TestA', self.user_mrtest.username, 400, 400)
        self.budget_b = Budget(
            'TestB', self.user_mrtest.username, 100.0, 100.0)

    def test_add_budget(self):
        budget_repository.add_budget(self.budget_a)
        all_budgets = budget_repository.fetch_all()

        self.assertEqual(len(all_budgets), 1)
        self.assertEqual(all_budgets[0].name, self.budget_a.name)

    def test_fetch_all(self):
        budget_repository.add_budget(self.budget_a)
        budget_repository.add_budget(self.budget_b)
        all_budgets = budget_repository.fetch_all()

        self.assertEqual(len(all_budgets), 2)
        self.assertEqual(all_budgets[0].name, self.budget_a.name)
        self.assertEqual(all_budgets[1].name, self.budget_b.name)

    def test_find_by_username(self):
        budget_repository.add_budget(self.budget_a)

        budgets = budget_repository.find_by_username(self.user_mrtest.username)

        self.assertEqual(budgets[0].username, self.user_mrtest.username)

    def test_update_current_amount(self):
        budget_repository.add_budget(self.budget_a)
        budget_id = self.budget_a.id
        budget_repository.update_current_amount(200, budget_id)
        budget = (budget_repository.fetch_all())[0]

        self.assertEqual(str(budget.c_amount), '200.0')

    def test_delete_one(self):
        budget_repository.add_budget(self.budget_a)
        budget_repository.add_budget(self.budget_b)

        budget_b_id = self.budget_b.id
        budget_repository.delete_one(budget_b_id)
        budgets = budget_repository.fetch_all()

        user_budgets = budget_repository.find_by_username('MrTest')

        self.assertEqual(len(user_budgets),1)
        self.assertEqual(len(budgets), 1)

    def test_find_by_id(self):
        budget_repository.add_budget(self.budget_a)
        budget_id = self.budget_a.id

        budget = budget_repository.find_by_id(budget_id)
        self.assertEqual(budget.name, self.budget_a.name)
