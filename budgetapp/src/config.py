import os
from dotenv import load_dotenv

directory = os.path.dirname(__file__)

BUDGET_FILENAME = os.getenv('BUDGET_FILENAME') or budgets.csv
BUDGET_FILE_PATH = os.path.join(directory, '..', 'data', BUDGET_FILENAME)

PURCHASE_FILENAME = os.getenv('PURCHASE_FILENAME') or purchases.csv
PURCHASE_FILE_PATH = os.path.join(directory,'..','data', PURCHASE_FILENAME)

DATABASE_FILENAME = os.getenv('DATABASE_FILENAME') or 'database.sqlite'
DATABASE_FILE_PATH = os.path.join(dirname, '..', 'data', DATABASE_FILENAME)