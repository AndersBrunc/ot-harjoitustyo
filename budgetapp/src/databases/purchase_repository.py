from entities.purchase import Purchase
from db_connection import get_database_connection

def get_purchase_by_row(self):
    return Purchase(row['category'], row['amount'], row['user'], row['comment']) if row else None

class PurchaseRepository:
    '''Class of the purchase-repository
    '''

    def __init__(self, connection):
        '''class constructor

        Args:
            connection: database connection object

        '''
        self._connection = connection

    def fetch_all(self):
        '''Returns all purchases
        Returns:
            list of Purchase-objects
        '''
        cursor = self._connection.cursor()
        cursor.execute('select * from purchases')
        rows = cursor.fetchall()

        return list(map(get_purchase_by_row, rows))

    def find_by_username(self, username):
        '''Finds purchase based on username

        Args:
            username: the user the search is based on

        Returns:
            The list of purchases as Purchase-objects if in existance, otherwhise None

        '''
        all_purchases = self.fetch_all()
        new = filter(
            lambda purchase: purchase and purchase.user.username == username,
            all_purchases
        )
        return list(new)
        
    def find_by_category(self, category, username):
        '''Finds purchase based on category and username
        '''
        user_purchases = self.find_by_username(username)
        categorized = filter(
            lambda purchase: purchase and purchase.category == category,
            user_purchases
        )
        return list(categorized)

    def add_purchase(self, purchase):
        '''Saves a purchase in the purchase-database
        Args:
            purchase: Purchase-object that will be saved

        '''
        cursor = self._connection.cursor()
        cursor.execute(
            'insert into purchases (category,amount,username,comment,p_id) values (?,?,?,?,?)',
            (purchase.name, purchase.amount, purchase.username, purchase.comment, purchase.id)
        )
        self._connection.commit()

        return purchase

    def delete_one(self, p_id):
        '''Deletes specific purchase

        Args:
            p_id: id of the deleted purchase

        '''
        cursor = self._connection.cursor()
        cursor.execute('delete from purchases where p_id = ?', (p_id,))
        self._connection.commit()

    def delete_all(self):
        '''Deletes all purchases
        '''
        cursor = self._connection.cursor()
        cursor.execute('delete from purchases')
        self._connection.commit()

purchase_repository = PurchaseRepository(get_database_connection())

