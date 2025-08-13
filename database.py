from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_type = "SQLite"

if database_type == "SQLite":
    # SQLite database URL for SQLAlchemy
    # Can be left as it is, if no blog.db file is found it shall be created automatically
    SQLALCHEMY_DATABASE_URL = "sqlite:///./BlogAPI/blog.db"
    # Create the SQLAlchemy engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
elif database_type == "PostgreSQL":
    # Postgres database URL for SQLAlchemy
    # Here you will have to provide the correct database URL depending on your setup
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:<password>@localhost:5432/APIBlog"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
else:
    raise ValueError("Unsupported database type.")

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