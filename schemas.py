from pydantic import BaseModel, EmailStr
from typing import List, Optional, Literal
from datetime import datetime

class BlogBase(BaseModel):
    """
    Shared properties for blog models.
    """
    title: str
    body: str
    published: bool = True

class Blog(BlogBase):
    """
    Blog model for creating and updating blogs.
    """
    class Config:
        orm_mode = True

class User(BaseModel):
    """
    Schema for user creation.
    """
    name: str
    email: EmailStr
    password: str

class ShowUserSmall(BaseModel):
    """
    Schema for displaying basic user information.
    """
    name: str
    email: EmailStr
    created_at: datetime  # Use datetime for proper serialization
    id : int

    class Config:
        orm_mode = True

class ShowUser(ShowUserSmall):
    """
    Schema for displaying a user with their blogs.
    """
    blogs: List[Blog] = []

class ShowBlog(BlogBase):
    """
    Schema for displaying a blog with its creator's basic info.
    """
    creator: ShowUserSmall
    created_at: datetime  # Use datetime for proper serialization

    class Config:
        orm_mode = True
        # Allows reading data from ORM objects, not just dicts.
        
class BlogWithVotes(BaseModel):
    """
    Schema for displaying a blog with its creator's basic info and vote count.
    """
    Blog: ShowBlog
    votes: int

    class Config:
        orm_mode = True

class Login(BaseModel):
    """
    Schema for user login.
    The email is used as the username.
    """
    username: EmailStr
    password: str

class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for data extracted from a JWT token.
    """
    username: Optional[EmailStr] = None
    id : Optional[int] = None
    
class Vote(BaseModel):
    """
    Schema for creating a vote.
    """
    blog_id: int
    direction: Literal[0, 1]  # 1 for upvote, 0 for removing vote

    class Config:
        orm_mode = True