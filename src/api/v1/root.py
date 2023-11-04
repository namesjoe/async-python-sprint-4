from fastapi import APIRouter

from logger import setup_logger, get_logger

setup_logger('server.log')
logger = get_logger('server')
router = APIRouter()


@router.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Short links here!"}
