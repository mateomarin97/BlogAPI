from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from BlogAPI.database import Base

class Blog(Base):
    """
    SQLAlchemy model for the 'blogs' table.

    Attributes:
        id (int): Primary key, unique identifier for the blog.
        title (str): Title of the blog post.
        body (str): Content/body of the blog post.
        user_id (int): Foreign key referencing the creator (User).
        creator (User): Relationship to the User who created the blog.
    """
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    rating = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    creator = relationship("User", back_populates="blogs")

class User(Base):
    """
    SQLAlchemy model for the 'users' table.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user (unique).
        password (str): Hashed password of the user.
        blogs (List[Blog]): Relationship to the blogs created by the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    blogs = relationship("Blog", back_populates="creator")