from datetime import timedelta
from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from BlogAPI import schemas, models
from BlogAPI.hashing import Hash
from BlogAPI.JWTtoken import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


def generate_jwt_token(request: OAuth2PasswordRequestForm, db: Session) -> schemas.Token:
    """Generate a JWT access token for a valid user.

    Args:
        request (OAuth2PasswordRequestForm): Form data containing username (email) and password.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Token: An object containing the generated access token and token type.

    Raises:
        HTTPException: If the username does not exist or the password is incorrect.
    """
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": request.username, "id": user.id}, expires_delta=expires)

    return schemas.Token(access_token=token, token_type="bearer")
