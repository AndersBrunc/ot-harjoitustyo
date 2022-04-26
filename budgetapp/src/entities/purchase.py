import uuid


class Purchase:
    '''Class for purchases

    Attributes:
        budget_id: string, represents the budget affected by the purchase
        category: string, represents the purchased item(s) category
        amount: float, represents the receipt amount
        username: string, represnts users username
        comment:
                optinal, defaults to empty string "".
                string, represents the users comment on the purchase
        p_id: string, represents purchase-id
    '''

    def __init__(self, budget_id, category, amount, username, comment, p_id=None):
        '''Class constructor, creates a purchase

        Args:
            budget_id: string, represents the budget affected by the purchase
            category: string, represents the purchased item(s) category
            amount: float, represents the receipt amount
            username: string, represnts users username
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
        self.username = username
        self.comment = comment
        self.budget_id = budget_id
