from fastapi import APIRouter, Depends, status
from BlogAPI import schemas
from BlogAPI.database import get_db
from BlogAPI.repository import authentication as auth_repo
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_repo.Generate_JWT_Token(request, db)