from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

import models
import schemas
import crud
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Library Management API",
    description="A simple library management system API",
    version="1.0.0"
)


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Library Management API",
        "endpoints": {
            "authors": "/authors/",
            "books": "/books/",
            "docs": "/docs"
        }
    }


# Author Endpoints
@app.post("/authors/", response_model=schemas.AuthorResponse, status_code=201)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    """Create a new author."""
    try:
        return crud.create_author(db=db, author=author)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Author with this name already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/authors/", response_model=List[schemas.AuthorResponse])
def list_authors(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
        db: Session = Depends(get_db)
):
    """Retrieve a paginated list of authors."""
    authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def get_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    """Retrieve a single author by ID."""
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


# Book Endpoints
@app.post("/authors/{author_id}/books/", response_model=schemas.BookResponse, status_code=201)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    """Create a new book for a specific author."""
    # Check if author exists
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    try:
        return crud.create_book(db=db, book=book, author_id=author_id)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Database integrity error while creating book"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/books/", response_model=List[schemas.BookWithAuthor])
def list_books(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
        author_id: Optional[int] = Query(None, description="Filter books by author ID"),
        db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of books.
    Optionally filter by author_id.
    """
    books = crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
    return books
