from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

import models
import schemas
import crud
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="API for managing authors and books"
)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Author endpoints
@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    # Check if author with same name exists
    existing_authors = crud.get_authors(db, skip=0, limit=100)
    for existing in existing_authors:
        if existing.name.lower() == author.name.lower():
            raise HTTPException(
                status_code=400,
                detail="Author with this name already exists"
            )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=100,
        description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db)
):
    """Retrieve a list of authors with pagination"""
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorWithBooks)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Retrieve a single author by ID"""
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(
    author_id: int,
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    """Update an author"""
    db_author = crud.update_author(db, author_id=author_id, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author and all their books"""
    db_author = crud.delete_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return None


# Book endpoints
@app.post("/books/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book for a specific author"""
    # Check if author exists
    author = crud.get_author(db, author_id=book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = Query(
        0, ge=0, description="Number of records to skip"
    ),
    limit: int = Query(
        100, ge=1, le=100,
        description="Maximum number of records to return"
    ),
    author_id: Optional[int] = Query(
        None, description="Filter books by author ID"
    ),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of books with pagination.
    Optionally filter by author ID.
    """
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books


@app.get("/books/{book_id}", response_model=schemas.BookWithAuthor)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieve a single book by ID"""
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    """Update a book"""
    # Check if author exists
    author = crud.get_author(db, author_id=book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return None


# Additional endpoint: Get books by specific author
@app.get(
    "/authors/{author_id}/books/", response_model=List[schemas.Book]
)
def read_author_books(
    author_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve all books for a specific author"""
    # Check if author exists
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    books = crud.get_books_by_author(
        db, author_id=author_id, skip=skip, limit=limit
    )
    return books


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
