from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> list[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_authors(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_authors(author=author, db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
    author_id: int = None
) -> list[schemas.Book]:
    return crud.get_all_books(
        db=db, author_id=author_id, skip=skip, limit=limit,
    )


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}/", response_model=schemas.Book)
def read_single_book(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book_by_id(db=db, author_id=author_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
