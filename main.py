from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from library import models
from library.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(db: Session = Depends(get_db)):
    """Retrieve a list of books with pagination"""
    return crud.get_all_books(db=db)


@app.post("/books/", response_model=schemas.BookList)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    """Create a new book"""
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400, detail="Such title for Book already exist"
        )

    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(db: Session = Depends(get_db)):
    """Retrieve a list of authors with pagination"""
    return crud.get_all_authors(db=db)


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    """Create a new author"""
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exist"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorList)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Retrieve a single author by ID"""
    db_author = crud.get_author_by_id(db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookList)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    """Create a new book for a specific author."""
    return crud.create_author_book(db=db, book=book, author_id=author_id)
