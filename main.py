from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.engine import SessionLocal
import schemas
import crud

# define FastAPI application object
app = FastAPI()


# dependency function to manage database sessions
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoint to create a new author
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author name already registered")
    return crud.create_author(db=db, author=author)


# API endpoint to retrieve a list of authors with pagination (skip, limit)
@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.Author]:
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


# API endpoint to retrieve a single author by ID
@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> Optional[schemas.Author]:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# API endpoint to create a new book for a specific author
@app.post("/authors/books/", response_model=schemas.Book)
def create_book_for_author(
    book: schemas.BookCreate, db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.create_book(db=db, book=book)


# API endpoint to retrieve a list of books with pagination (skip, limit)
@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.Book]:
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


# API endpoint to filter books by author ID
@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[schemas.Book]:
    books = crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    if not books:
        raise HTTPException(status_code=404, detail="Author has no books")
    return books
