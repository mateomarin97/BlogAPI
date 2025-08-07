from fastapi import status, HTTPException
from BlogAPI import schemas, models
from BlogAPI.hashing import Hash
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from BlogAPI.JWTtoken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

def Generate_JWT_Token(request: OAuth2PasswordRequestForm, db: Session):
    actual_user = db.query(models.User).filter(models.User.email == request.username).first()
    if not actual_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    actual_password = actual_user.password
    is_correct = Hash.verify(request.password, actual_password)
    if not is_correct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    #generate a JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")