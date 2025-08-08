from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional
from BlogAPI.schemas import TokenData

# Secret key for JWT encoding/decoding (generate with: openssl rand -hex 32)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the token (e.g., user info).
        expires_delta (Optional[timedelta]): Optional expiration time delta.

    Returns:
        str: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception) -> TokenData:
    """
    Verify a JWT token and extract the token data.

    Args:
        token (str): JWT token string.
        credentials_exception: Exception to raise if verification fails.

    Returns:
        TokenData: Token data containing the username.

    Raises:
        credentials_exception: If token is invalid or username is missing.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data