from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from logger import setup_logger, get_logger

setup_logger('server.log')
logger = get_logger('server')
router = APIRouter()


@router.get("/ping")
async def ping_db(db):
    logger.info("Ping DB endpoint accessed")
    try:
        db.execute("SELECT 1")  # Just a simple query to check database connectivity
        return {"message": "Database is accessible"}
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database is not accessible")
