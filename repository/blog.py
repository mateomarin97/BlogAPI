from fastapi import status, HTTPException, Response
from sqlalchemy.orm import Session

from BlogAPI import schemas, models

def get_all_blogs(db: Session):
    """Retrieve all blogs from the database."""
    return db.query(models.Blog).all()

def get_blog(id: int, db: Session):
    """Retrieve a blog by ID or raise 404 if not found."""
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

def create_blog(request: schemas.Blog, db: Session, user_id: int):
    """Create a new blog linked to the given user ID."""
    new_blog = models.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id: int, db: Session, user_id: int):
    """Delete a blog if the requesting user is the owner."""
    blog = get_blog(id, db)
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this blog")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update_blog(id: int, request: schemas.Blog, db: Session, user_id: int):
    """Update a blog's title and body if the requesting user is the owner."""
    blog = get_blog(id, db)
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this blog")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog
