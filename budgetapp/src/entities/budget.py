import uuid

class Budget:

    '''Class that describes a budget
    
    Attributes:
        b_id: string, represents the budget-id
        user: User-object, represents the user
        name: string, represents name of the budget
        original_amount: float, represents the original budget amount 
        left_amount: float, represents the amount that is still left in the budget

    '''

    def __init__(self,b_id=None,user,name,original_amount,left_amount):
       
        '''Class construcor, makes a new budget.
    
        Args:
            b_id: 
                optional, defaults to uuid
                string, represents the budget-id
            user: User-object, represents the user
            name: string, represents name of the budget
            original_amount: float, represents the original budget amount 
            left_amount: float, represents the amount left in the budget
        '''

        self.id=b_id or str(uuid.uuid4())
        self.user=user
        self.name=name
        self.original_amount=original_amount
        self.left_amount=left_amount