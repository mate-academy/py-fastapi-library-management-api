from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine, Base, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description=("A simple API for managing authors and their books "
                 "in a library."),
    version="1.0.0",
)

@app.post("/authors/",
          response_model=schemas.Author,
          status_code=status.HTTP_201_CREATED)
def create_author_endpoint(author: schemas.AuthorCreate,
                           db: Session = Depends(get_db)):
    db_author = crud.create_author(db=db, author=author)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists"
        )
    return db_author

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors_endpoint(skip: int = 0,
                          limit: int = 100,
                          db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return db_author

@app.post("/authors/{author_id}/books/",
          response_model=schemas.Book,
          status_code=status.HTTP_201_CREATED)
def create_book_for_author_endpoint(author_id: int,
                                    book: schemas.BookCreate,
                                    db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=List[schemas.Book])
def read_books_endpoint(skip: int = 0,
                        limit: int = 100,
                        author_id: Optional[int] = None,
                        db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book
