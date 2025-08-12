from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    """
    Shared properties for blog models.
    """
    title: str
    body: str
    published: bool = True
    rating: Optional[int] = None

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
    email: str
    password: str

class ShowUserSmall(BaseModel):
    """
    Schema for displaying basic user information.
    """
    name: str
    email: str

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

    class Config:
        orm_mode = True
        # Allows reading data from ORM objects, not just dicts.

class Login(BaseModel):
    """
    Schema for user login.
    The email is used as the username.
    """
    username: str
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
    username: Optional[str] = None