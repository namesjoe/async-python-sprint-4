import pytest
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.models.model import URL


Base = declarative_base()


@pytest.mark.asyncio
async def test_create_url():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    url = URL(
        full_url="http://example.com",
        short_url_id="test-short-url",
        user_id=1,
        deleted=False
    )
    session.add(url)
    session.commit()

    retrieved_url = session.query(URL).filter_by(short_url_id="test-short-url").first()
    assert retrieved_url is not None
    assert retrieved_url.full_url == "http://example.com"

    session.close()
    Base.metadata.drop_all(engine)


@pytest.mark.asyncio
async def test_delete_url():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    url = URL(
        full_url="http://example.com",
        short_url_id="test-short-url",
        user_id=1,
        deleted=False
    )
    session.add(url)
    session.commit()

    # Delete the URL
    session.delete(url)
    session.commit()

    retrieved_url = session.query(URL).filter_by(short_url_id="test-short-url").first()
    assert retrieved_url is None

    session.close()
    Base.metadata.drop_all(engine)

