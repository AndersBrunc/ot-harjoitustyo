from pathlib import Path
from entities.purchase import Purchase
from config import PURCHASE_FILE_PATH


class PurchaseRepository:
    '''Class of the purchases
    '''

    def __init__(self, path):
        '''Class constructor
            Args:
            path: path to the location for saving the purchases
        '''
        self._path = path

    def _check_file_exists(self):
        Path(self._path).touch()

    def _write(self, purchases):
        self._check_file_exists()

        with open(self._path, 'w', encoding='utf-8') as file:
            for purchase in purchases:
                row = f'{purchase.id};{purchase.category};{purchase.amount};{purchase.user};{purchase.comment}'
                file.write(row+'\n')

    def _read(self):
        purchases = []
        self._check_file_exists()

        with open(self._path, encoding='utf-8') as file:
            for row in file:
                row = row.replace('\n', '')
                row_piece = row.split(';')

                p_id = row_piece[0]
                category = row_piece[1]
                amount = row_piece[2]
                user = row_piece[3]
                comment = row_piece[4]
                purchases.append(
                    Purchase(category, amount, user, comment, p_id))

            return purchases

    def fetch_all(self):
        '''Returns all purchases
        Returns:
            list of Purchase-objects
        '''
        return self._read()

    def add_purchase(self, purchase):
        '''Saves a purchase in the purchase-database
        Args:
            purchase: Purchase-object that will be saved

        '''
        all_purchases = self.fetch_all()
        all_purchases.append(purchase)
        self._write(all_purchases)

        return purchase

    def delete_one(self, p_id):
        '''Deletes specific purchase

        Args:
            p_id: id of the deleted purchase

        '''
        self._check_file_exists()
        all_purchases = self.fetch_all()
        edited_list = filter(
            lambda purchase: purchase.id != p_id, all_purchases)
        self._write(edited_list)

    def delete_all(self):
        '''Deletes all purchases
        '''
        self._write([])

    def find_by_username(self, username):

        purchases = self.fetch_all()

        user_purchases = filter(
            lambda purchase: purchase.user and
            purchase.user.username == username, purchases
        )
        return list(user_purchases)

    def find_by_category(self, category, username):

        user_purchases = self.find_by_username(username)
        categorized = filter(
            lambda purchase: purchase.category and
            purchase.category == category, user_purchases
        )
        return list(categorized)


purchase_repository = PurchaseRepository(PURCHASE_FILE_PATH)
