import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Depends, security, HTTPException, status

import models, schemas, crud
from database import SessionLocal


JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_REFRESH_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e9"
# JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
# JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
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


def get_payload_from_data(data: dict, expire_delta: int) -> dict:
    payload = {
        field: val for field, val in data.items() if field != "date_created"
    }
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expire_delta)
    return payload


def create_access_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    payload = get_payload_from_data(
        user_obj.dict(), ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    payload = get_payload_from_data(
        user_obj.dict(), REFRESH_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(payload, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_tokens(user: models.User):
    return {
        "access_token": create_access_token(user=user),
        "refresh_token": create_refresh_token(user=user)
    }


def authenticate_user(
    email: str,
    password: str,
    db: Session
):
    user = crud.get_user_by_email(email=email, db=db)
    if not user or not verify_password(password, user.hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user


def get_data_from_payload(token: str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=ALGORITHM
        )
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email of password"
        )
    return payload


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2schema),
):
    user_data = get_data_from_payload(token)
    return crud.get_user(db=db, user_id=user_data["id"])
