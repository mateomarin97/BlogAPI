from fastapi import APIRouter, Depends, status, Response, HTTPException
from BlogAPI import schemas, models
from BlogAPI.database import get_db
from sqlalchemy.orm import Session
from typing import List
from BlogAPI.repository import blog
from BlogAPI.oauth2 import get_current_token

router = APIRouter(prefix="/blog", tags=["Blogs"])

def get_current_user_id(current_token: schemas.TokenData, db: Session):
    user = db.query(models.User).filter(models.User.email == current_token.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.id

@router.get("/", response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db), current_token: schemas.TokenData = Depends(get_current_token)):
    return blog.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_token: schemas.TokenData = Depends(get_current_token)):
    user_id = get_current_user_id(current_token, db)
    return blog.create(request, db, user_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_token: schemas.TokenData = Depends(get_current_token)):
    user_id = get_current_user_id(current_token, db)
    return blog.delete(id, db, user_id)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_token: schemas.TokenData = Depends(get_current_token)):
    user_id = get_current_user_id(current_token, db)
    return blog.update(id, request, db, user_id)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model= schemas.ShowBlog)
def get_blog(id: int,db: Session = Depends(get_db), current_token: schemas.TokenData = Depends(get_current_token)):
   return blog.get(id, db)