class Budget:

    '''Class that describes a budget
    
    Attributes:
        user: User-object, represents the user
        name: string, represents name of the budget
        original_amount: float, represents the original budget amount 
        left_amount: float, represents the amount that is still left in the budget

    '''

    def __init__(self,user,name=str,orignal_amount=float):
       
        '''Class construcor, makes a new budget.
    
        Args:
            user: User-object, represents the user
            name: string, represents name of the budget
            original_amount: float, represents the original budget amount 

        '''
       
        self.user=user
        self.name=name
        self.original_amount=original_amount
        self.left_amount=original_amount