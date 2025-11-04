from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
from database import SessionLocal, engine
from models import Base
from schemas import (
    CreateAuthorRequest,
    CreateBookRequest,
    GetAuthorResponse,
    GetBookResponse,
)

app = FastAPI()


def create_db_tables():
    Base.metadata.create_all(bind=engine)


create_db_tables()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def root():
    return {"message": "connected"}


@app.post("/authors/", response_model=GetAuthorResponse)
def create_author(
    CreateAuthorRequest: CreateAuthorRequest, db: Session = Depends(get_db)
):
    return crud.create_author(author=CreateAuthorRequest, db=db)


@app.get("/authors/", response_model=list[GetAuthorResponse])
def read_authors(
            skip: int = 0,
            limit: int = 10,
            db: Session = Depends(get_db)
        ):
    return crud.get_authors(skip, limit, db=db)


@app.get("/authors/{id}", response_model=GetAuthorResponse)
def read_author(id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(id=id, db=db)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=GetBookResponse)
def create_book(
        request_book: CreateBookRequest,
        db: Session = Depends(get_db)
        ):
    return crud.create_book(book=request_book, db=db)


@app.get("/books/", response_model=list[GetBookResponse])
def read_books(
    skip: int = 0, limit: int = 10,
    author_id: int = None,
    db: Session = Depends(get_db)
):
    return crud.get_books(skip, limit, author_id, db=db)


@app.get("/books/{id}", response_model=GetBookResponse)
def read_book(id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(id=id, db=db)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
