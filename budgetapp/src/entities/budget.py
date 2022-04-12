import uuid


class Budget:

    '''Class that describes a budget

    Attributes:
        name: string, represents name of the budget
        user: User-object, represents the user
        og_amount: float, represents the original budget amount 
        c_amount: float, represents the amount that is still currently left in the budget
        b_id: string, represents the budget-id

    '''

    def __init__(self, name, user, og_amount, c_amount, b_id=None):
        '''Class construcor, makes a new budget.

        Args:
            name: string, represents name of the budget
            user: User-object, represents the user
            og_amount: float, represents the original budget amount 
            c_amount: float, represents the amount left in the budget
            b_id: 
                optional, defaults to uuid
                string, represents the budget-id
        '''

        self.id = b_id or str(uuid.uuid4())
        self.user = user
        self.name = name
        self.og_amount = og_amount
        self.c_amount = c_amount
