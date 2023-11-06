from os.path import join, dirname

from dotenv import load_dotenv

from src.utils.utils_funcs import get_db_url
from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int
    JWT_SECRET_KEY: str
    DBNAME: str
    HOST_URL: str

    class Config:
        env_file = ".env"


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

settings = Settings()

SERVER_HOST = settings.SERVER_HOST
SERVER_PORT = settings.SERVER_PORT
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
DATABASE_URL = get_db_url(settings.DBNAME, settings.HOST_URL)
