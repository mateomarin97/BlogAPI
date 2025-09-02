from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from BlogAPI import schemas
from BlogAPI.database import get_db
from BlogAPI.repository import user as user_repo
from BlogAPI.oauth2 import get_current_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
    summary="Create a new user",
    response_description="The created user"
)
def create_user(
    request: schemas.User,
    db: Session = Depends(get_db)
):
    """
    Create a new user.

    Args:
        request (schemas.User): The user data from the request.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.ShowUser: The created user object.
    """
    return user_repo.create(request, db)

@router.get(
    "/{id}",
    response_model=schemas.ShowUser,
    summary="Get a user by ID",
    response_description="The requested user"
)
def get_user(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a user by ID.

    Args:
        id (int): The ID of the user to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        schemas.ShowUser: The requested user object.
    """
    return user_repo.get(id, db)

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletes current user",
    response_description="User deleted successfully"
)
def delete_user(
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token)
):
    """
    Deletes the currently logged in user.

    Args:
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        None
    """
    user_id = current_token.id
    user_repo.delete(user_id, db)