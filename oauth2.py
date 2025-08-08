from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from BlogAPI.schemas import TokenData
import BlogAPI.JWTtoken as jwt_module

# OAuth2 scheme for extracting the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Dependency to retrieve and verify the current user's JWT token.

    Args:
        token (str): JWT token extracted from the Authorization header.

    Returns:
        TokenData: Token data containing the username.

    Raises:
        HTTPException: If the token is invalid or credentials cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return jwt_module.verify_token(token, credentials_exception)

