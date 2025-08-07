#from sqlmodel import Field, Session, SQLModel, create_engine, select
#from typing import Annotated
#from fastapi import Depends

#sqlite_file_name = "blog.db"
#sqlite_url = f"sqlite:///./{sqlite_file_name}"

#connect_args = {"check_same_thread": False}
#engine = create_engine(sqlite_url, connect_args=connect_args)

#def create_db_and_tables():
    #SQLModel.metadata.create_all(engine)


#def get_session():
    #with Session(engine) as session:
        #yield session


#SessionDep = Annotated[Session, Depends(get_session)]

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./BlogAPI/blog.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()