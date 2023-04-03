from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
) -> list[models.Author]:
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.create_author(db=db, author=author)
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[models.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/authors/{author_id}/books/",
         response_model=list[schemas.Book])
def read_books_by_author(
        author_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    books = (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .join(models.Author)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return books
