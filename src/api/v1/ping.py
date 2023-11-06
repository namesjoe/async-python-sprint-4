from logger import setup_logger, get_logger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db


setup_logger('server.log')
logger = get_logger('server')
router = APIRouter()

@router.get("/ping")
async def ping_db(db: AsyncSession = Depends(get_db)):
    logger.info("Ping DB endpoint accessed")
    try:
        await db.execute("SELECT 1")  # Just a simple query to check database connectivity
        return {"message": "Database is accessible"}
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database is not accessible")
