from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Library written by FastAPI"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)[skip:skip + limit]


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, author_name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0, limit: int = 10,
        db: Session = Depends(get_db),
        author_id: int | None = None,
):
    return crud.get_book_list(
        db=db, author_id=author_id
    )[skip:skip + limit]


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def read_single_book(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_author_id(db=db, author_id=author_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book
