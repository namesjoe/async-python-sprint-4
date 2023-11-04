from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logger import setup_logger, get_logger
from src.core.config import DATABASE_URL

setup_logger('server.log')
logger = get_logger('server')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
