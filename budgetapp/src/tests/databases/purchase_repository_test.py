import unittest
from databases.purchase_repository import purchase_repository
from entities.purchase import Purchase
from entities.user import User
from entities.budget import Budget


class TestPurchaseRepository(unittest.TestCase):
    def setUp(self):
        purchase_repository.delete_all()
        self.user_mrtest = User('MrTest', 'test123', 1000, 500, 200)
        self.budget_test = Budget(
            'Testbudget', self.user_mrtest.username, 100, 100)
        self.purchase_a = Purchase(
            self.budget_test.id, 'Food', 10, self.user_mrtest.username, '')
        self.purchase_b = Purchase(
            self.budget_test.id, 'Food', 5.5, self.user_mrtest.username, 'Lidl')
        self.purchase_c = Purchase(
            self.budget_test.id, 'Misc', 80, self.user_mrtest.username, 'random stuff')

    def test_add_purchase(self):
        purchase_repository.add_purchase(self.purchase_a)
        all_purchases = purchase_repository.fetch_all()

        self.assertEqual(len(all_purchases), 1)
        self.assertEqual(all_purchases[0].amount, self.purchase_a.amount)

    def test_fetch_all(self):
        purchase_repository.add_purchase(self.purchase_a)
        purchase_repository.add_purchase(self.purchase_b)

        all_purchases = purchase_repository.fetch_all()

        self.assertEqual(len(all_purchases), 2)
        self.assertEqual(all_purchases[0].amount, self.purchase_a.amount)
        self.assertEqual(all_purchases[1].amount, self.purchase_b.amount)

    def test_find_by_username(self):
        purchase_repository.add_purchase(self.purchase_a)
        purchases = purchase_repository.find_by_username(
            self.purchase_a.username)

        self.assertEqual(purchases[0].username, self.purchase_a.username)

    def test_find_by_category(self):
        purchase_repository.add_purchase(self.purchase_a)
        purchase_repository.add_purchase(self.purchase_b)
        purchase_repository.add_purchase(self.purchase_c)

        purchases = purchase_repository.find_by_category('Food', 'MrTest')

        self.assertEqual(len(purchases), 2)
        self.assertEqual(purchases[0].amount, self.purchase_a.amount)
        self.assertEqual(purchases[1].amount, self.purchase_b.amount)

    def test_delete_one(self):
        purchase_repository.add_purchase(self.purchase_a)
        purchase_repository.add_purchase(self.purchase_b)

        purchase_b_id = self.purchase_b.id
        purchase_repository.delete_one(purchase_b_id)
        purchases = purchase_repository.fetch_all()

        self.assertEqual(len(purchases), 1)
