from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session

import schemas
import crud
import db.models
from db.database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/check-db")
def check_db():
    inspector = inspect(engine)
    return {"tables": inspector.get_table_names()}


@app.get("/")
def read_root()-> dict:
    return {"Hello": "Mate!"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> list[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_from_id(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> list[schemas.Book]:
    return crud.get_book_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def get_books_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_books_by_author_id(db=db, author_id=author_id)


@app.post("/book/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> schemas.Book:
    db_author = crud.get_author_by_id(db, book.author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = crud.get_book_by_author_and_title(db, book.title, book.author_id)
    if db_book is not None:
        raise HTTPException(
            status_code=400,
            detail="Book with this author already exists"
        )

    return crud.create_book(db=db, book=book)