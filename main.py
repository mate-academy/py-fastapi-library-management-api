from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import (
    BookList,
    BookCreate,
    AuthorList,
    AuthorCreate
)
from models import Book, Author
from crud import (
    get_book_list,
    get_book,
    create_book,
    get_author_list,
    get_author,
    create_author
)


app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[BookList])
def read_books(
    author_id: int = None,
    db: Session = Depends(get_db)
) -> list[Book]:
    return get_book_list(db, author_id)


@app.get("/books/{book_id}/", response_model=BookList)
def read_book(book_id: int, db: Session = Depends(get_db)) -> Book | None:
    book = get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=400,
            detail="Book not found"
        )

    return book


@app.post("/books/", response_model=BookCreate)
def write_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
) -> Book:
    return create_book(db, book_data)


@app.get("/authors/", response_model=list[AuthorList])
def read_authors(db: Session = Depends(get_db)) -> list[Author]:
    return get_author_list(db)


@app.get("/authors/{author_id}/", response_model=AuthorList)
def read_author(
    author_id: int,
    db: Session = Depends(get_db)
) -> Author | None:
    author = get_author(db, author_id)

    if not author:
        raise HTTPException(
            status_code=400,
            detail="Author not found"
        )

    return author


@app.post("/authors/", response_model=AuthorCreate)
def write_author(
    author_data: AuthorCreate,
    db: Session = Depends(get_db)
) -> Author:
    author = db.query(Author).filter(Author.name == author_data.name)

    if author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )

    return create_author(db, author_data)
