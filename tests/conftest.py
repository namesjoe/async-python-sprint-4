import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testing.postgresql import Postgresql

from app import app

from src.db.db_setup import SessionLocal

# Create a temporary PostgreSQL database for testing
postgresql = Postgresql()

TEST_DATABASE_URL = postgresql.dsn()

@pytest.fixture(scope="module")
def test_client():
    # override to use the testing database
    app.dependency_overrides[SessionLocal] = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(TEST_DATABASE_URL))
    client = TestClient(app)
    yield client
    # Clean up after the test
    client.__enter__().app.dependency_overrides.pop(SessionLocal)

@pytest.fixture(scope="function")
def test_db():
    db = SessionLocal()
    yield db
    db.close()

# Clean up the temporary database after the tests
def pytest_sessionfinish(session, exitstatus):
    postgresql.stop()
