from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.check_authors_name(db=db, author_name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author is already registered"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[schemas.Author]:
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_author_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.Book]:
    books = crud.get_all_books(db, skip=skip, limit=limit)
    return books


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)) -> list[schemas.Book]:
    db_books = crud.filter_book_by_author(db=db, author_id=author_id)

    if not db_books:
        raise HTTPException(status_code=404, detail="Author's id is not found")

    return db_books
