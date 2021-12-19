from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.oauth import create_access_token
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(
        models.User.email == user_credentials.username)

    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    password_is_valid = utils.verify(user_credentials.password, user.password)

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id})

    return {"access_token": access_token, "type": "bearer"}
