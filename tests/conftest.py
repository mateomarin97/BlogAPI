import pytest
from fastapi.testclient import TestClient
from BlogAPI.main import app
from BlogAPI.database import get_db, Base
from BlogAPI.tests.database import engine, TestingSessionLocal

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
    user_data = {"name": "Nathan", "email": "mateomarin97@hotmail.com", "password": "123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user_data["id"] = response.json().get("id")
    return user_data