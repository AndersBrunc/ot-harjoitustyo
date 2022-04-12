
from entities.budget import budget
from pathlib import Path
from config import PURCHASE_FILE_PATH

class PurchaseRepository:
    '''Class of the purchases
    '''
    def __init__(self,path):
    '''Class constructor
    Args: 
        path: path to the location for saving the purchases
    '''
        self._path=path
    
