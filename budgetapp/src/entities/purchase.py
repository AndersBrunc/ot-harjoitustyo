import uuid


class Purchase:
    '''Class for purchases

    Attributes:
        category: string, represents the purchased item(s) category
        amount: float, represents the receipt amount
        user: User-object, represnts user
        comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
        p_id: string, represents purchase-id
    '''

    def __init__(self, category, amount, user, comment, p_id=None):
        '''Class constructor, creates a purchase

        Args:
            category: string, represents the purchased item(s) category
            amount: float, represents the receipt amount
            user: User-object, represnts user
            comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
            p_id:
                optional, defaults to generated uuid
                string, represents purchase-id
        '''
        self.id = p_id or str(uuid.uuid4())
        self.category = category
        self.amount = amount
        self.user = user
        self.comment = comment
