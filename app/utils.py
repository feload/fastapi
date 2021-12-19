from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(strs: str):
    return pwd_context.hash(strs)


def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
