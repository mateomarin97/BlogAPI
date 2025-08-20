from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from BlogAPI import schemas, models
from BlogAPI.database import get_db
from BlogAPI.repository import blog as blog_repo
from BlogAPI.oauth2 import get_current_token

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

@router.get(
    "/",
    response_model=List[schemas.ShowBlog],
    summary="Get all blogs",
    response_description="List of all blogs"
)
def get_blogs(
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token),
    limit: int = 10,
    offset: int = 0
):
    """
    Retrieve all published blogs and all unpublished blogs belonging to the current user.

    Args:
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        List[schemas.ShowBlog]: List of all blogs.
    """
    user_id = current_token.id
    return blog_repo.get_all_blogs(db, user_id, limit, offset)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new blog",
    response_description="The created blog"
)
def create_blog(
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token)
):
    """
    Create a new blog post.

    Args:
        request (schemas.Blog): Blog data from the request.
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        models.Blog: The created blog object.
    """
    user_id = current_token.id
    return blog_repo.create_blog(request, db, user_id)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a blog",
    response_description="No content"
)
def delete_blog(
    id: int,
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token)
):
    """
    Delete a blog post by ID.

    Args:
        id (int): Blog ID.
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        None
    """
    user_id = current_token.id
    return blog_repo.delete_blog(id, db, user_id)

@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a blog",
    response_description="The updated blog"
)
def update_blog(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token)
):
    """
    Update a blog post by ID.

    Args:
        id (int): Blog ID.
        request (schemas.Blog): Updated blog data.
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        models.Blog: The updated blog object.
    """
    user_id = current_token.id
    return blog_repo.update_blog(id, request, db, user_id)

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    summary="Get a blog by ID",
    response_description="The requested blog"
)
def get_blog(
    id: int,
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token)
):
    """
    Retrieve a blog post by ID.

    Args:
        id (int): Blog ID.
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        schemas.ShowBlog: The requested blog object.
    """
    user_id = current_token.id
    return blog_repo.get_blog(id, db, user_id)