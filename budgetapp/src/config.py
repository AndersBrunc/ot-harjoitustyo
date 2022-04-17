import os
from dotenv import load_dotenv

directory = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(directory, '..', '.env'))
except FileNotFoundError:
    pass

DATABASE_FILENAME = os.getenv('DATABASE_FILENAME') or 'database.sqlite'
DATABASE_FILE_PATH = os.path.join(directory, '..', 'data', DATABASE_FILENAME)
