class Purchase:
    '''Class for purchases

    Attributes:
        amount: float, represents the receipt amount
        category: string, represents the purchased item(s) category
        comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
    '''
    def __init__(self,amount,category,comment):
        '''Class constructor, creates a purchase

        Args:
            amount: float, represents the receipt amount
            category: string, represents the purchased item(s) category
            comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
        '''

        self.amount=amount
        self.category=category
        self.comment=comment