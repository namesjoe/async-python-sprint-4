from os.path import join, dirname

from dotenv import load_dotenv

from src.core.settings import Settings
from src.utils.utils_funcs import get_db_url

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

settings = Settings()  # Create an instance of the Settings class

SERVER_HOST = settings.SERVER_HOST
SERVER_PORT = settings.SERVER_PORT
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
DATABASE_URL = get_db_url(settings.DBNAME, settings.HOST_URL)
