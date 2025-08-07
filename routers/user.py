from fastapi import APIRouter, status, Depends, HTTPException
from BlogAPI import schemas, models
from BlogAPI.database import  get_db
from sqlalchemy.orm import Session
from BlogAPI.hashing import Hash
from BlogAPI.repository import user

router = APIRouter(prefix= "/user" ,tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)

@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get(id, db)