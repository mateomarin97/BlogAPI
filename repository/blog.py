from fastapi import status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, select
from typing import Optional

from BlogAPI import schemas, models

def get_all_blogs(
    db: Session,
    user_id: int,
    limit: int,
    offset: int,
    search: Optional[str] = None
):
    """
    Retrieve blogs with vote counts.

    Includes:
    - All published blogs.
    - All unpublished blogs belonging to the current user.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the current user.
        limit (int): Maximum number of blogs to return.
        offset (int): Number of blogs to skip.
        search (Optional[str]): Filter blogs whose titles contain this string.

    Returns:
        list[tuple[models.Blog, int]]: List of (Blog, vote_count) tuples.
    """
    stmt = (
        select(
            models.Blog,
            func.count(models.Vote.blog_id).label("votes")
        )
        .join(models.Vote, models.Blog.id == models.Vote.blog_id, isouter=True)
        .group_by(models.Blog.id)
        .filter(
            or_(
                models.Blog.published,
                and_(
                    ~models.Blog.published,
                    models.Blog.user_id == user_id
                )
            )
        )
        .limit(limit)
        .offset(offset)
    )

    if search:
        stmt = stmt.filter(models.Blog.title.contains(search))

    return db.execute(stmt).all()

def get_blog(id: int, db: Session, user_id: int):
    """Retrieve a blog by ID or raise 404 if not found."""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None or (blog.published == False and blog.user_id != user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

def create_blog(request: schemas.Blog, db: Session, user_id: int):
    """Create a new blog linked to the given user ID."""
    # request.model_dump() gives us the blog data as a dictionary
    new_blog = models.Blog(**request.model_dump(), user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id: int, db: Session, user_id: int):
    """Delete a blog if the requesting user is the owner."""
    blog = get_blog(id, db, user_id)
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this blog")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update_blog(id: int, request: schemas.Blog, db: Session, user_id: int):
    """Update a blog's fields if the requesting user is the owner."""
    blog = get_blog(id, db, user_id)
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this blog")
    update_data = request.model_dump()
    for key, value in update_data.items():
        setattr(blog, key, value)
    db.commit()
    db.refresh(blog)
    return blog
