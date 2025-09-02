from fastapi import status, HTTPException, Response
from BlogAPI import schemas, models
from sqlalchemy.orm import Session
from BlogAPI.hashing import Hash

def create(request: schemas.User, db: Session):
    """
    Create a new user in the database.

    Args:
        request (schemas.User): The user data from the request.
        db (Session): SQLAlchemy database session.

    Returns:
        models.User: The newly created user object.
    """
    request.password = Hash.bcrypt(request.password)
    new_user = models.User(
        **request.model_dump()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(id: int, db: Session):
    """
    Retrieve a user by ID.

    Args:
        id (int): The ID of the user to retrieve.
        db (Session): SQLAlchemy database session.

    Returns:
        models.User: The user object if found.

    Raises:
        HTTPException: If the user is not found.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def delete(id: int, db: Session):
    """
    Delete a user by ID.

    Args:
        id (int): The ID of the user to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        None

    Raises:
        HTTPException: If the user is not found.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)