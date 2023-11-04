from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.models.model import URL

Base = declarative_base()


def create_test_url(db: Session):
    test_url = URL(
        full_url="http://google.com",
        short_url_id="test123",
        user_id=1,
        deleted=False
    )
    db.add(test_url)
    db.commit()
    db.refresh(test_url)
    return test_url
