import uuid

class Purchase:
    '''Class for purchases

    Attributes:
        p_id: string, represents purchase-id
        product: string, represents the product bought
        category: string, represents the purchased item(s) category
        amount: float, represents the receipt amount
        comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
    '''
    def __init__(self,p_id=None,product,category,amount,comment):
        '''Class constructor, creates a purchase

        Args:
            p_id:
                optional, defaults to generated uuid
                string, represents purchase-id
            product: string, represents the product bought
            category: string, represents the purchased item(s) category
            amount: float, represents the receipt amount
            comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
        '''
        self.id = p_id or str(uuid.uuid4())
        self.product = product
        self.category = category
        self.amount = amount
        self.comment = comment