from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BlogAPI.config import settings

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
