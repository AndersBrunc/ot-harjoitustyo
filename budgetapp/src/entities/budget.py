import uuid


class Budget:

    '''Class that describes a budget

    Attributes:
        b_id: string, represents the budget-id
        user: User-object, represents the user
        name: string, represents name of the budget
        og_amount: float, represents the original budget amount 
        c_amount: float, represents the amount that is still currently left in the budget

    '''

    def __init__(self, b_id=None, user, name, og_amount, c_amount):
        '''Class construcor, makes a new budget.

        Args:
            b_id: 
                optional, defaults to uuid
                string, represents the budget-id
            user: User-object, represents the user
            name: string, represents name of the budget
            og_amount: float, represents the original budget amount 
            c_amount: float, represents the amount left in the budget
        '''

        self.id = b_id or str(uuid.uuid4())
        self.user = user
        self.name = name
        self.og_amount = og_amount
        self.c_amount = c_amount
