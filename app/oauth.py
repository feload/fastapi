from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, models

# secret_key
SECRET_KEY = "abc6udyu788wn37yjf73j37d6wuhd73teoe0l2ls0fiwjkdefye8"

# algorithm
ALGORITHM = "HS256"

# expiration time
ACCESS_TOKEN_EXPIRATION_MINUTES = 120

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="login", tokenUrl="login")


def create_access_token(data: dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    data_copy.update({"exp": expire})

    encoded_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = decoded_jwt.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credetials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials.")

    token_data = verify_access_token(
        token, credentials_exception=credetials_exception)

    user = db.query(models.User).filter(
        models.User.id == token_data.id).first()

    return user
