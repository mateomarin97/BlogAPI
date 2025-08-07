from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
import BlogAPI.JWTtoken as jwt_module
from BlogAPI.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return jwt_module.verify_token(token, credentials_exception)
    
   