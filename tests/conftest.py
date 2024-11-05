import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.dependencies.database import get_db
from app.db import Base
from app.main import app
from tests.utils import create_user_for_test


# In-memory SQLite configuration for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


# SQLite engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


# Specific local session for tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create all tables at the start of testing
Base.metadata.create_all(bind=engine)



@pytest.fixture(scope="function")
def db():
    """
    Creates a database session for the tests. It starts a transaction at the 
    beginning and rolls it back at the end, so that each test has a clean environment.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()



@pytest.fixture(scope="function")
def client(db):
    """
    Client to interact with the API during tests. Override the 
    get_db to use the test database instead of the production database.
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client



@pytest.fixture(scope="function")
def auth_user_token(client):
    """
    Fixture to create a test user and return their authentication token.
    """
    # Create a user for testing
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Login to get an access token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)

    assert response.status_code == 200, f"Failed to authenticate, status code: {response.status_code}"
    token = response.json().get("access_token")
    assert token, "Authentication failed: 'access_token' not found in response."

    return token
