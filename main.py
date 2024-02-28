from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from database import  engine

# Create database tables using SQLAlchemy models
models.Base.metadata.create_all(bind=engine)

# Define FastAPI application object
app = FastAPI()


# Dependency function to manage database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoints

# Create a new author
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


# Retrieve a list of authors with pagination (skip, limit)
@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


# Retrieve a single author by ID
@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# Create a new book for a specific author
@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book, author_id)


# Retrieve a list of books with pagination (skip, limit)
@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


# Filter books by author ID
@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db, author_id)
