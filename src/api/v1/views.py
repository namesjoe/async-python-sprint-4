# views.py
from logger import get_logger
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from src.db.database import get_current_user, get_db
from src.models.model import DBUser
from src.schemas.response import PostResponse
from src.core.config import SERVER_HOST, SERVER_PORT
from src.api.v1.services import shorten_url, delete_url, redirect_to_original_url


router = APIRouter()
logger = get_logger('server')


@router.post("/shorten/", name="shorten")
async def shorten_url_enpoint(url: str,
                               user: DBUser = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    logger.info(f"Shorten URL endpoint accessed by user: {user.username}")

    short_url_id = shorten_url(db, url, user.id)

    return {"short_url": f"http://{SERVER_HOST}:{SERVER_PORT}/{short_url_id}"}


@router.delete("/{short_url_id}", response_model=PostResponse)
async def delete_url_endpoint(short_url_id: str,
                              db: Session = Depends(get_db),
                              user: DBUser = Depends(get_current_user)):
    logger.info(f"Delete URL endpoint accessed for short URL: {short_url_id}")

    delete_url(db, short_url_id, user)

    return PostResponse(message="URL deleted successfully")


@router.get("/{short_url_id}")
async def redirect_to_original_url_endpoint(short_url_id: str, request: Request, db: Session = Depends(get_db)):
    logger.info(f"Redirect endpoint accessed for short URL: {short_url_id}")

    full_url = redirect_to_original_url(db, short_url_id, request)

    return RedirectResponse(full_url, status_code=307)
