from fastapi import status, Response, HTTPException
from BlogAPI import schemas, models
from sqlalchemy.orm import Session

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def get(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

def create(request: schemas.Blog, db: Session, user_id: int):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id: int, db: Session, user_id: int):
    blog = get(id, db)
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this blog")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update(id: int, request: schemas.Blog, db: Session, user_id: int):
    blog = get(id, db)
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this blog")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog