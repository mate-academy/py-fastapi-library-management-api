from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from db.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
        db: Session = Depends(get_db),
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 3,
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=list[schemas.AuthorRead])
def read_authors(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_all_authors(db=db, author_id=author_id)[0]

    if db_author is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_author


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_name = crud.get_author_by_name(db=db, name=author.name)

    if db_name:
        raise HTTPException(
            status_code=400,
            detail="Such name already exists in the database"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(
        db: Session = Depends(get_db),
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 3,
):
    return crud.get_books_list(db, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=list[schemas.BookRead])
def read_books(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_books_list(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book

@app.post("/books/", response_model=schemas.BookCreate)
def create_books(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    # db_name = crud.create_book(db=db, title=book.title)
    #
    # if db_name:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Such name already exists in the database"
    #     )
    return crud.create_book(db=db, book=book)
