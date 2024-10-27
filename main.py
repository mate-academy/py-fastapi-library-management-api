from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import Author, Book

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# AUTHOR endpoints
@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> list[Author]:
    authors = crud.get_all_authors(db)
    return authors[skip: skip + limit]


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.put("/authors/{author_id}/", response_model=schemas.AuthorUpdate)
def update_author(
    author_id: int,
    author: schemas.AuthorUpdate,
    db: Session = Depends(get_db)
) -> Author:
    db_author = crud.update_author(db, author_id, author)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db)
) -> Author:
    db_author = crud.get_author_by_id(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    if not crud.delete_author(db, author_id):
        raise HTTPException(status_code=400, detail="Failed to delete author")

    return db_author


# BOOK endpoints
@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> Book:
    db_author = crud.get_author_by_id(db, book.author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> list[Book]:
    books = crud.get_all_books(db)
    return books[skip: skip + limit]


@app.get("/books/author/{author_id}/", response_model=schemas.Book)
def read_books_by_author_id(
    author_id: int,
    db: Session = Depends(get_db)
) -> list[Book]:
    book = crud.get_books_by_author(db, author_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="No books found for this author"
        )

    return book


@app.put("/books/{book_id}/", response_model=schemas.BookUpdate)
def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: Session = Depends(get_db)
) -> Book:
    db_book = crud.update_book(db, book_id, book_data)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> Book:
    db_book = crud.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not crud.delete_book(db, book_id):
        raise HTTPException(status_code=400, detail="Failed to delete book")

    return db_book
