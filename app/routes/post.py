from typing import List, Optional
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth
from ..database import get_db

router = APIRouter(
    tags=["Post"]
)


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user), limit: int = 10, page: int = 1, search: Optional[str] = ""):

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(
            search)).limit(limit).offset((page - 1) * limit).all()

    return result


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def post_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")

    return post


@router.delete("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post id not found.")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"data": "Post deleted"}


@router.put('/posts/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post_data: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, defailt="Post not found.")

    post_query.update(post_data.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
