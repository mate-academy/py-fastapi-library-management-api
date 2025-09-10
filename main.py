from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import Author, Book, AuthorCreate, BookCreate
from crud import (
    get_all_authors,
    get_all_books,
    get_author_by_id,
    create_author_db,
    create_book_db,
    get_book_by_id
)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Wellcome to the Library"}


@app.get("/authors/", response_model=List[Author])
def get_authors(db: Session = Depends(get_db)) -> List[Author]:
    return get_all_authors(db)


@app.get("/authors/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)) -> Author:
    return get_author_by_id(db=db, id=author_id)


@app.post("/authors/", response_model=Author)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)
) -> Author:
    return create_author_db(db=db, author=author)


@app.get("/books/", response_model=List[Book])
def get_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
) -> List[Book]:
    return get_all_books(db=db, author_id=author_id)


@app.get("/books/", response_model=Book)
def get_book(
        author_id: int,
        db: Session = Depends(get_db),
):
    return get_book_by_id(db=db, id=author_id)


@app.post("/books/", response_model=Book)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db),
):
    return create_book_db(db=db, book=book)
