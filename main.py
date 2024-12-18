from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import AuthorCreate, BookCreate, AuthorOut, BookOut
from crud import (
    create_author,
    get_authors,
    get_author_by_id,
    create_book,
    get_books,
)

# Initialize the FastAPI app
app = FastAPI()

# Створення таблиць бази даних
Base.metadata.create_all(bind=engine)  # Create database tables

# Ендпоінти


@app.post("/authors", response_model=AuthorOut)
def add_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)


@app.get("/authors", response_model=list[AuthorOut])
def list_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[AuthorOut]:
    return get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)) -> AuthorOut:
    author = get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return author


@app.post("/authors/{author_id}/books", response_model=BookOut)
def add_book(
    author_id: int, book: BookCreate, db: Session = Depends(get_db)
) -> BookOut:
    return create_book(db, author_id, book)


@app.get("/books", response_model=list[BookOut])
def list_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int = None,
    db: Session = Depends(get_db)
) -> list[BookOut]:
    return get_books(db, skip, limit, author_id)
