from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./BlogAPI/blog.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency that provides a SQLAlchemy database session.

    Yields:
        Session: SQLAlchemy database session.

    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()