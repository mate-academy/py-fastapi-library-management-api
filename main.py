from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Library Management API",
    description="A simple library management system for authors and books",
    version="1.0.0"
)


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Library Management API"}


# Author endpoints
@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_new_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    # Check if author with same name already exists
    existing_author = db.query(models.Author).filter(models.Author.name == author.name).first()
    if existing_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
        db: Session = Depends(get_db)
):
    """Retrieve a list of authors with pagination"""
    authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorWithBooks)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Retrieve a single author by ID with their books"""
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author_details(
        author_id: int,
        author_update: schemas.AuthorUpdate,
        db: Session = Depends(get_db)
):
    """Update an author's details"""
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if new name already exists (if name is being updated)
    if author_update.name and author_update.name != db_author.name:
        existing_author = db.query(models.Author).filter(
            models.Author.name == author_update.name
        ).first()
        if existing_author:
            raise HTTPException(status_code=400, detail="Author with this name already exists")

    return crud.update_author(db=db, author_id=author_id, author_update=author_update)


@app.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author_record(author_id: int, db: Session = Depends(get_db)):
    """Delete an author"""
    db_author = crud.delete_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# Book endpoints
@app.post("/books/", response_model=schemas.Book, status_code=201)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book for a specific author"""
    # Check if author exists
    db_author = crud.get_author(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book)


# UPDATED: Use BookWithSimpleAuthor instead of BookWithAuthor for list
@app.get("/books/", response_model=List[schemas.BookWithSimpleAuthor])
def read_books(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
        author_id: Optional[int] = Query(None, description="Filter books by author ID"),
        db: Session = Depends(get_db)
):
    """Retrieve a list of books with pagination and optional author filter"""
    books = crud.get_books_with_authors(db=db, skip=skip, limit=limit, author_id=author_id)
    return books


# Keep BookWithAuthor for single book retrieval (full details)
@app.get("/books/{book_id}", response_model=schemas.BookWithAuthor)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a single book by ID with author details"""
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book_details(
        book_id: int,
        book_update: schemas.BookUpdate,
        db: Session = Depends(get_db)
):
    """Update a book's details"""
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if new author exists (if author_id is being updated)
    if book_update.author_id is not None:
        db_author = crud.get_author(db=db, author_id=book_update.author_id)
        if db_author is None:
            raise HTTPException(status_code=404, detail="Author not found")

    return crud.update_book(db=db, book_id=book_id, book_update=book_update)


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book_record(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    db_book = crud.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/authors/{author_id}/books/", response_model=List[schemas.Book])
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    """Get all books by a specific author"""
    # Check if author exists
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_books_by_author(db=db, author_id=author_id)
