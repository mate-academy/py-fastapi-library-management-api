from starlette import status
from fastapi import FastAPI, Depends, Path
from crud import (
    create_author,
    create_book,
    get_authors,
    retrieve_author,
    get_books,
    get_books_by_author_id
)
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import (
    CreateAuthor,
    CreateBook,
    Author,
    Book
)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=Author
)
def author_create(author: CreateAuthor, db: Session = Depends(get_db)):
    return create_author(db, author)


@app.get(
    "/authors/",
    status_code=status.HTTP_200_OK,
    response_model=list[Author]
)
def authors_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_authors(db, skip, limit)


@app.get(
    "/authors/{author_id}/",
    status_code=status.HTTP_200_OK,
    response_model=Author
)
def author_retrieve(author_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return retrieve_author(db, author_id)


@app.post(
    "/book/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book
)
def book_create(book: CreateBook, db: Session = Depends(get_db), ):
    return create_book(db, book)


@app.get(
    "/books/",
    status_code=status.HTTP_200_OK,
    response_model=list[Book]
)
def books_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_books(db, skip, limit)


@app.get(
    "/books/{author_id}/",
    status_code=status.HTTP_200_OK,
    response_model=list[Book]
)
def retrieve_book_by_author_id(author_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return get_books_by_author_id(db, author_id)
