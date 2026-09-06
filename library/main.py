from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends

from library.database import Base, engine, SessionLocal
from library.crud import (
    create_author,
    get_authors,
    get_author,
    create_book,
    get_books,
    get_book,
)
from library.schemas import (
    AuthorCreate,
    AuthorResponse,
    BookResponse,
    BookCreate
)

Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=AuthorResponse)
def create_author_endpoint(author: AuthorCreate, db=Depends(get_db)):
    return create_author(db, author)


@app.get("/authors/", response_model=List[AuthorResponse])
def get_authors_endpoint(db=Depends(get_db), skip: int = 0, limit: int = 100):
    return get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author_endpoint(author_id: int, db=Depends(get_db)):
    author = get_author(db, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/books/{author_id}/", response_model=BookResponse)
def create_book_endpoint(book: BookCreate, author_id: int, db=Depends(get_db)):
    author = get_author(db, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return create_book(db, book, author_id)


@app.get("/books/", response_model=List[BookResponse])
def get_books_endpoint(
    db=Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
):
    return get_books(db, skip, limit, author_id)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_endpoint(book_id: int, db=Depends(get_db)):
    book = get_book(db, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
