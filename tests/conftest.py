import pytest
from fastapi.testclient import TestClient
from BlogAPI.main import app
from BlogAPI.database import get_db, Base
from BlogAPI.tests.database import engine, TestingSessionLocal
from BlogAPI.JWTtoken import create_access_token

@pytest.fixture()
def session():
    """
    Fixture that provides a SQLAlchemy database session for testing.
    """
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    """
    Fixture that provides a test client for the FastAPI application, and sets up the database.
    """
    def override_get_db():
        """
        Dependency that provides a SQLAlchemy database session.

        Yields:
            Session: SQLAlchemy database session.

        Ensures the session is closed after use.
        """
        try:
            yield session
        finally:
            session.close()
            
    #This swaps the original get_db with the override for testing
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture()
def test_user(client):
    """Create a test user.

    Args:
        client (TestClient): The test client.

    Returns:
        dict: The created user data.
    """
    user_data = {"name": "Nathan", "email": "mateomarin97@hotmail.com", "password": "123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user_data["id"] = response.json().get("id")
    return user_data

@pytest.fixture()
def token(test_user):
    """Create a test token for the test user.

    Args:
        test_user (dict): The test user data.

    Returns:
        str: The access token.
    """
    return create_access_token(data={"sub": test_user["email"], "id": test_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    """Create an authorized test client with the token.

    Args:
        client (TestClient): The test client.
        token (str): The access token.

    Returns:
        TestClient: The authorized test client.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

