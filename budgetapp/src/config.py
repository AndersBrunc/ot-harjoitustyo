import os
from dotenv import load_dotenv

directory = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(directory, '..', '.env'))
except FileNotFoundError:
    pass


BUDGET_FILENAME = os.getenv('BUDGET_FILENAME')
BUDGET_FILE_PATH = os.path.join(directory, '..', 'data', BUDGET_FILENAME)

PURCHASE_FILENAME = os.getenv('PURCHASE_FILENAME')
PURCHASE_FILE_PATH = os.path.join(directory, '..', 'data', PURCHASE_FILENAME)

DATABASE_FILENAME = os.getenv('DATABASE_FILENAME') or 'database.sqlite'
DATABASE_FILE_PATH = os.path.join(directory, '..', 'data', DATABASE_FILENAME)
