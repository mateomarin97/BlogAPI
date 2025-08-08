from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from BlogAPI import schemas
from BlogAPI.database import get_db
from BlogAPI.repository import authentication as auth_repo

router = APIRouter(tags=["Authentication"])

@router.post(
    "/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and return JWT token",
    response_description="JWT access token"
)
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT token.

    Args:
        request (OAuth2PasswordRequestForm): The login form containing username and password.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.Token: JWT access token if authentication is successful.
    """
    return auth_repo.generate_jwt_token(request, db)