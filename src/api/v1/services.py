# services.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.model import URL
from src.utils.utils_funcs import generate_random_string
from src.models.model import URLAccess


def delete_url(db: Session, short_url_id: str, user):
    url = db.query(URL).filter(URL.short_url_id == short_url_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if url.deleted:
        raise HTTPException(status_code=410, detail="URL already deleted")

    if user.username != "admin" and url.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this URL")

    db.commit()

def shorten_url(db: Session, url: str, user_id: int):
    short_url_id = generate_random_string()
    new_url = URL(full_url=url, short_url_id=short_url_id, user_id=user_id)
    db.add(new_url)
    db.commit()
    return short_url_id


def redirect_to_original_url(db: Session, short_url_id: str, request):
    url = db.query(URL).filter(URL.short_url_id == short_url_id).first()
    if not url or url.deleted:
        raise HTTPException(status_code=404, detail="URL not found")

    access_data = URLAccess(url_id=url.id,
                            user_agent=request.headers.get("User-Agent"),
                            client_ip=request.client.host)
    db.add(access_data)
    db.commit()

    return url.full_url
