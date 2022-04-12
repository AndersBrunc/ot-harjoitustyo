import os
from dotenv import load_dotenv

directory = os.path.dirname(__file__)

PURCHASE_FILE_PATH = os.path.join(directory,'..','databases', PURCHASE_FILENAME)