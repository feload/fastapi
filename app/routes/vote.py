from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from .. import oauth, schemas, models

router = APIRouter(tags=["Votes"])


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    existing_vote = vote_query.first()

    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="The user has already voted that post")
        else:
            new_vote = models.Vote(post_id=vote.post_id,
                                   user_id=current_user.id)
            db.add(new_vote)
            db.commit()

            return {"detail": "Vote registered"}
    else:
        if existing_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"detail": "Vote registered"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post vote not found")
