from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/")
def read_authors(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Author]:
    authors = crud.get_authors(skip=skip, limit=limit, db=db)
    return authors


@app.get("/authors/{author_id}")
def read_author(
        author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/")
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This author already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/")
def read_books(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Book]:
    books = crud.get_books(skip=skip, limit=limit, db=db)
    return books


@app.get("/books/{book_id}")
def get_book(
        book_id: int, db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/books/")
def create_book(
        book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="This book already exist"
        )

    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}/")
def get_books_by_author_id(
        author_id: int, db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_book_by_author_id(db=db, author_id=author_id)
