import pytest
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your SQLAlchemy models
Base = declarative_base()


class URL(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    full_url = Column(String)
    short_url_id = Column(String)
    user_id = Column(Integer)
    deleted = Column(Boolean, default=False)


# test database and session
@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


# Example test for creating a URL
def test_create_url(db_session):
    url = URL(
        full_url="http://example.com",
        short_url_id="test-short-url",
        user_id=1,
        deleted=False
    )
    db_session.add(url)
    db_session.commit()

    retrieved_url = db_session.query(URL).filter_by(short_url_id="test-short-url").first()
    assert retrieved_url is not None
    assert retrieved_url.full_url == "http://example.com"


# Example test for deleting a URL
def test_delete_url(db_session):
    url = URL(
        full_url="http://example.com",
        short_url_id="test-short-url",
        user_id=1,
        deleted=False
    )
    db_session.add(url)
    db_session.commit()

    # Delete the URL
    db_session.delete(url)
    db_session.commit()

    retrieved_url = db_session.query(URL).filter_by(short_url_id="test-short-url").first()
    assert retrieved_url is None
