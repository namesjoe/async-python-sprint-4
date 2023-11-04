from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.db_setup import SessionLocal
from src.models.model import DBUser
from src.models.model import URL
from src.core.security import verify_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_url_by_short_url_id(db: Session, short_url_id: str):
    return db.query(URL).filter(URL.short_url_id == short_url_id).first()


def create_url(db: Session, url: str, short_url_id: str, user_id: int):
    new_url = URL(full_url=url, short_url_id=short_url_id, user_id=user_id)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url


def get_user_by_username(db: Session, username: str):
    return db.query(DBUser).filter(DBUser.username == username).first()


def get_current_user(token: str = Depends(verify_token)) -> DBUser:
    token_data = verify_token(token)
    user = get_user_by_username(token_data.username)
    return user
