from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from BlogAPI import schemas, models


def validate_blog_is_published(db: Session, blog_id: int) -> None:
    """
    Validate that a blog exists and is published.

    Args:
        db (Session): SQLAlchemy database session.
        blog_id (int): ID of the blog to validate.

    Raises:
        HTTPException: If the blog does not exist or is not published.
    """
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )
    if not blog.published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blog is not published"
        )


def create_vote(vote: schemas.Vote, db: Session, user_id: int):
    """
    Create or delete a vote depending on the direction.

    Args:
        vote (schemas.Vote): Vote data from the request.
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user creating or deleting the vote.

    Returns:
        dict: Message indicating the result of the operation.
    """
    # Always validate blog first
    validate_blog_is_published(db, vote.blog_id)

    db_vote = db.query(models.Vote).filter(
        models.Vote.blog_id == vote.blog_id,
        models.Vote.user_id == user_id
    ).first()

    if vote.direction == 1:  # Upvote
        if db_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vote already exists"
            )

        new_vote = models.Vote(blog_id=vote.blog_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}

    else:  # Remove vote
        if not db_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not found"
            )

        db.delete(db_vote)
        db.commit()
        return {"message": "Vote deleted successfully"}
