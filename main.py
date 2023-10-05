from typing import Type

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from models import Author, Book

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.create_author(db=db, author=author)
    return db_author


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[Author]]:
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(
    author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)
) -> Type[Author] | None:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    updated_author = crud.update_author(db=db, author_id=author_id, author=author)
    return updated_author


@app.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)) -> Type[Author]:
    deleted_author = crud.delete_author(db=db, author_id=author_id)
    if deleted_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return deleted_author


@app.get("/authors/{author_id}/books/", response_model=list[Type[schemas.Book]])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[schemas.Book]]:
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


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[Type[schemas.Book]])
def get_books(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Type[schemas.Book]]:
    books = db.query(models.Book).join(models.Author).offset(skip).limit(limit).all()
    return books


@app.post("/books", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
) -> Type[Book]:
    db_book = crud.update_book(db=db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Type[Book]:
    deleted_book = crud.delete_book(db=db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
