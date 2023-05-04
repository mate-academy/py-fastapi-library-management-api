import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Depends, security, HTTPException, status

import models, schemas, crud
from database import SessionLocal


JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2schema = security.OAuth2PasswordBearer("token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    user_dict = user_obj.dict()
    del user_dict["date_created"]
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_dict.update({"exp": expire})
    token = jwt.encode(user_dict, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return token


def create_refresh_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    user_dict = user_obj.dict()
    del user_dict["date_created"]
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    user_dict.update({"exp": expire})
    token = jwt.encode(user_dict, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return token


def authenticate_user(
    email: str,
    password: str,
    db: Session
):
    user = crud.get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not verify_password(
        plain_password=password,
        hashed_password=user.hashed_pass
    ):
        return False
    return user


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2schema),
):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=ALGORITHM
        )
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        user = db.query(models.User).get(payload["id"])
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email of password"
        )
    return schemas.User.from_orm(user)
