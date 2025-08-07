from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    title: str
    body: str
    
class Blog(BlogBase):
    class Config:
        orm_mode = True
    
        
class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowUser_small(BaseModel):
    name: str
    email: str
    class Config:
        orm_mode = True
    
    
class ShowUser(ShowUser_small):
    blogs: List[Blog] = []
        
#This class is used to determine how the data will be returned to the user.    
class ShowBlog(BlogBase):
    creator: ShowUser_small
    class Config:
        orm_mode = True
        # This allows the model to read data even if it is not a dictionary, 
        # such as when it is an ORM model instance.
        
        # This is necessary for FastAPI to convert SQLAlchemy models to Pydantic models.
        
class Login(BaseModel):
    #The email is the username for login.
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None