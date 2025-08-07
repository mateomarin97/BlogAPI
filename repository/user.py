from fastapi import status, HTTPException
from BlogAPI import schemas, models
from sqlalchemy.orm import Session
from BlogAPI.hashing import Hash

def create(request: schemas.User, db: Session):
    hashed_password = Hash.bcrypt(request.password)
    request.password = hashed_password
    # Create a new user instance
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user