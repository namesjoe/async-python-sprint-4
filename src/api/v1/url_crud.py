from fastapi import APIRouter, HTTPException, Request
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from logger import get_logger
from src.core.config import SERVER_HOST, SERVER_PORT
from src.db.database import get_current_user, get_db
from src.models.model import DBUser
from src.models.model import URL, URLAccess
from src.schemas.response import PostResponse
from src.utils.utils_funcs import generate_random_string

router = APIRouter()
logger = get_logger('server')


@router.post("/shorten/", name="shorten")
async def shorten_url(url: str,
                      user: DBUser = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    logger.info(f"Shorten URL endpoint accessed by user: {user.username}")

    short_url_id = generate_random_string()

    new_url = URL(full_url=url, short_url_id=short_url_id, user_id=user.id)
    db.add(new_url)
    db.commit()

    return {"short_url": f"http://{SERVER_HOST}:{SERVER_PORT}/{short_url_id}"}


@router.delete("/{short_url_id}", response_model=PostResponse)
async def delete_url(short_url_id: str,
                     db: Session = Depends(get_db),
                     user: DBUser = Depends(get_current_user)):
    # Check  user has permission to delete this URL
    url = db.query(URL).filter(URL.short_url_id == short_url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if url.deleted:
        raise HTTPException(status_code=410, detail="URL already deleted")

    if user.username != "admin" and url.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this URL")

    db.commit()

    return PostResponse(message="URL deleted successfully")


@router.get("/{short_url_id}")
async def redirect_to_original_url(short_url_id: str,
                                   request: Request,
                                   db: Session = Depends(get_db)):
    logger.info(f"Redirect endpoint accessed for short URL: {short_url_id}")

    url = db.query(URL).filter(URL.short_url_id == short_url_id).first()
    if not url or url.deleted:
        raise HTTPException(status_code=404, detail="URL not found")

    access_data = URLAccess(url_id=url.id,
                            user_agent=request.headers.get("User-Agent"),
                            client_ip=request.client.host)
    db.add(access_data)
    db.commit()

    return RedirectResponse(url.full_url, status_code=307)
