from sqlalchemy.orm import sessionmaker
import aiopg.sa
import asyncio


from logger import setup_logger, get_logger
from src.core.config import DATABASE_URL

setup_logger('server.log')
logger = get_logger('server')


async def create_async_engine():
    engine = await aiopg.sa.create_engine(DATABASE_URL)
    return engine

engine = asyncio.get_event_loop().run_until_complete(create_async_engine())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
