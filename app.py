from fastapi import APIRouter
from fastapi import FastAPI

from logger import setup_logger, get_logger
from src.api.v1 import root, user, status, views, ping
from src.db.db_setup import engine
from src.models.model import Base

Base.metadata.create_all(bind=engine)

setup_logger('server.log')
logger = get_logger('server')

app = FastAPI()
router = APIRouter()


app.include_router(root.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(status.router, prefix="/api/v1")
app.include_router(views.router, prefix="/api/v1")
app.include_router(ping.router, prefix="/api/v1")
