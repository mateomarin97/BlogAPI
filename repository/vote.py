from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from BlogAPI import schemas, models

def create_vote(vote: schemas.Vote, db: Session, user_id: int):
    """
    Create a new vote.

    Args:
        vote (schemas.Vote): Vote data from the request.
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user creating the vote.

    Returns:
        models.Vote: The created vote object.
    """
    #First we check if the vote already exists
    db_vote = db.query(models.Vote).filter(
        models.Vote.blog_id == vote.blog_id,
        models.Vote.user_id == user_id
    ).first()
    #In this case we create a vote
    if vote.direction == 1:
        #We check if the vote already exists
        if db_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vote already exists")
        #Now we check if the blog has been published
        db_blog = db.query(models.Blog).filter(models.Blog.id == vote.blog_id).first()
        if not db_blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        if not db_blog.published:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog is not published")
        db_vote = models.Vote(blog_id=vote.blog_id, user_id=user_id)
        db.add(db_vote)
        db.commit()
        return {"Message": "Vote created successfully"}
    #In the other case we erase the already created vote
    else:
        if db_vote:
            #We must check if the blog is published
            db_blog = db.query(models.Blog).filter(models.Blog.id == vote.blog_id).first()
            if not db_blog:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
            if not db_blog.published:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blog is not published")
            db.delete(db_vote)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        return {"Message": "Vote deleted successfully"}