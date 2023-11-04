from fastapi import APIRouter, HTTPException

from logger import get_logger
from src.db.database import get_user_by_username
from src.db.db_setup import SessionLocal
from src.models.model import URL, URLAccess

router = APIRouter()
logger = get_logger('server')


@router.get("/user/status")
async def get_user_statuses(user=get_user_by_username):
    db = SessionLocal()

    user_urls = db.query(URL).filter(URL.user_id == user.id).all()
    return {"user_urls": user_urls}


@router.get("/{short_url_id}/status")
async def get_url_status(
        short_url_id: str,
        full_info: bool = False,
        max_result: int = 10,
        offset: int = 0
):
    db = SessionLocal()

    url = db.query(URL).filter(URL.short_url_id == short_url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    query = db.query(URLAccess).filter(URLAccess.url_id == url.id)

    total_access_count = query.count()

    if full_info:
        access_info = query.order_by(URLAccess.access_time.desc()).offset(offset).limit(max_result).all()
        return {
            "total_access_count": total_access_count,
            "access_info": access_info
        }
    else:
        return {"total_access_count": total_access_count}
