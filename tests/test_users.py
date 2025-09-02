import pytest
from fastapi.testclient import TestClient
from BlogAPI.main import app
from BlogAPI import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BlogAPI.config import settings
from BlogAPI.database import get_db, Base

database_type = "PostgreSQL"

if database_type == "SQLite":
    # SQLite database URL for SQLAlchemy
    # Can be left as it is, if no blog.db file is found it shall be created automatically
    SQLALCHEMY_DATABASE_URL = "sqlite:///./BlogAPI/blog_test.db"
    # Create the SQLAlchemy engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
elif database_type == "PostgreSQL":
    # Postgres database URL for SQLAlchemy
    # Here you will have to provide the correct database URL depending on your setup
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
else:
    raise ValueError("Unsupported database type.")

# Create a configured "Session" class
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Dependency that provides a SQLAlchemy database session.

    Yields:
        Session: SQLAlchemy database session.

    Ensures the session is closed after use.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#This swaps the original get_db with the override for testing
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    """
    Fixture that provides a test client for the FastAPI application, and sets up the database.
    """
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)

@pytest.mark.parametrize("user_id", [(1),(2),(3)])
def test_read_users(user_id, client):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200 or response.status_code == 404
    assert isinstance(response.json(), dict)
    if response.status_code == 200:
        assert response.json().get("id") == user_id
        
def test_create_user(client):
    response = client.post("/users/", json={"name": "Test User", "email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    new_user = schemas.ShowUser.model_validate(response.json()) 
    assert new_user.id is not None
    