from fastapi import APIRouter, Depends, status
import BlogAPI.schemas as schemas
from sqlalchemy.orm import Session
from BlogAPI.repository import vote as vote_repo

from BlogAPI.database import get_db
from BlogAPI.oauth2 import get_current_token

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vote",
    response_description="The created vote"
)
def create_vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_token: schemas.TokenData = Depends(get_current_token)
):
    """
    Create a new vote.

    Args:
        vote (schemas.Vote): Vote data from the request.
        db (Session): SQLAlchemy database session.
        current_token (schemas.TokenData): Token data for authentication.

    Returns:
        json: message indicating the result of the vote creation.
    """
    user_id = current_token.id
    return vote_repo.create_vote(vote, db, user_id)