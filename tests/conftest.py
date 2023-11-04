import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app
from src.db.db_setup import SessionLocal


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    db = SessionLocal()
    yield db
    db.close()
