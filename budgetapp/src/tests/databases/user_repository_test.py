import unittest
from databases.users_repository import user_repository
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repository.delete_all()
        self.user_mrtest = User('MrTest', 'test123', 1000, 500, 200)
        self.user_testdude = User('Testdude', 'testing', 50, 20, 10)

    def test_create_user(self):
        user_repository.create_user(self.user_mrtest)
        all_users = user_repository.fetch_all()

        self.assertEqual(len(all_users), 1)
        self.assertEqual(all_users[0].username, self.user_mrtest.username)

    def test_fetch_all(self):
        user_repository.create_user(self.user_mrtest)
        user_repository.create_user(self.user_testdude)
        all_users = user_repository.fetch_all()

        self.assertEqual(len(all_users), 2)
        self.assertEqual(all_users[0].username, self.user_mrtest.username)
        self.assertEqual(all_users[1].username, self.user_testdude.username)

    def test_find_by_username(self):
        user_repository.create_user(self.user_mrtest)

        user = user_repository.find_by_username(self.user_mrtest.username)

        self.assertEqual(user.username, self.user_mrtest.username)

    def test_update_balance(self):
        user_repository.create_user(self.user_mrtest)
        new_balance = 200
        username = self.user_mrtest.username
        user_repository.update_balance(new_balance, username)
        balance = user_repository.find_by_username(username).balance

        self.assertEqual(new_balance, balance)

    def test_update_income(self):
        user_repository.create_user(self.user_mrtest)
        new_income = 200
        username = self.user_mrtest.username
        user_repository.update_income(new_income, username)
        income = user_repository.find_by_username(username).income

        self.assertEqual(new_income, income)

    def test_update_expenses(self):
        user_repository.create_user(self.user_mrtest)
        new_expenses = 200
        username = self.user_mrtest.username
        user_repository.update_expenses(new_expenses, username)
        expenses = user_repository.find_by_username(username).expenses

        self.assertEqual(new_expenses, expenses)
