import pytest
from fastapi.testclient import TestClient
from BlogAPI.main import app
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