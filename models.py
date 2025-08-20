from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship
from BlogAPI.database import Base

class Blog(Base):
    """
    SQLAlchemy model for the 'blogs' table.

    Attributes:
        id (int): Primary key, unique identifier for the blog.
        title (str): Title of the blog post.
        body (str): Content/body of the blog post.
        published (bool): Indicates if the blog is published.
        created_at (datetime): Timestamp when the blog was created (set automatically).
        rating (int, optional): Optional rating for the blog post.
        user_id (int): Foreign key referencing the creator (User).
        creator (User): Relationship to the User who created the blog.
    """
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    published = Column(Boolean, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    creator = relationship("User", back_populates="blogs")
    votes = relationship(
        "Vote",
        back_populates="blog",
        cascade="all, delete-orphan",   # makes ORM delete related votes
        passive_deletes=True            # let DB enforce FK ondelete
    )

class User(Base):
    """
    SQLAlchemy model for the 'users' table.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user (unique).
        password (str): Hashed password of the user.
        created_at (datetime): Timestamp when the user was created (set automatically).
        blogs (List[Blog]): Relationship to the blogs created by the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    blogs = relationship("Blog", back_populates="creator")
    votes = relationship(
        "Vote",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    blog_id = Column(Integer, ForeignKey('blogs.id', ondelete="CASCADE"), nullable=False, primary_key=True)

    user = relationship("User", back_populates="votes")
    blog = relationship("Blog", back_populates="votes")