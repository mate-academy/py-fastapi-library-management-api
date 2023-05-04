from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from schemas import Token
from security import (
    create_access_token,
    oauth_2_scheme,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
    authenticate_user
)
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=Token)
def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/sign-up", response_model=schemas.User)
async def create_user(user: schemas.User, db: Session = Depends(get_db), ):
    return crud.create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.User)
def read_users_me(
        token=Depends(oauth_2_scheme),
        db: Session = Depends(get_db)
):
    user = get_current_user(db=db, token=token)
    return user


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.delete("/author/{author_id}/", status_code=204)
def delete_single_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.delete_author(db=db, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int,
        db: Session = Depends(get_db),
        skip=2, limit=5,
        title=None,

):
    return crud.get_book_list(
        db=db,
        skip=skip,
        limit=limit,
        title=title,
        author_id=author_id
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)


@app.delete("/book/{book_id}/", status_code=204)
def delete_single_book(book_id: int, db: Session = Depends(get_db)):
    author = crud.get_book(db=db, book_id=book_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.delete_author(db=db, author_id=book_id)
