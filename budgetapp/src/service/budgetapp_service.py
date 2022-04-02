from entities.budget import Budget
from entities.user import User

class BudgetappService:
    '''The class of the application service'''

    def __init__(self):
        '''The constructor of the class, creates a new service session'''

        self._user = None

    def create_budget(self,user,name,amount):
        '''Creates a budget

        Args:
            user: User-object, represents user
            name: string, represents name of budget
            amount: float, represents the original budget amount

        Returns:
            budget as Budget-object
        '''


    def create_user(self,username,password):
        '''Creates a new user
        
        Args: 
            username: string, represents the user's username
            password: represents the user's password

        '''


    def login(self, username=str, password=str):
        '''Logs the user in 
        
        Args:
            username: string, represents the user's username
            password: string, represents the user's password
        
        Returns:
            user as User-object
        '''

    