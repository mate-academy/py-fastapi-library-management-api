from typing import Any, Generator

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

from crud import create_new_author, get_all_authors_by_skip_and_limit, get_author_by_id, create_book_for_author, \
    get_books_by_filtering
from db import schemas
from db.database import SessionLocal, Base, engine

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Any, Any, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return create_new_author(db, author)


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(skip: int | None, limit: int | None, db: Session = Depends(get_db)):
    return get_all_authors_by_skip_and_limit(db, skip, limit)


@app.get("/authors/{item_id}", response_model=schemas.Author)
def retrieve_author(item_id: int, db: Session = Depends(get_db)):
    return get_author_by_id(db, item_id)


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return create_book_for_author(db, book)


@app.get("/books", response_model=list[schemas.Book])
def get_books(skip: int | None = None, limit: int | None = None, author_id: int | None = None, db: Session = Depends(get_db)):
    return get_books_by_filtering(db, skip, limit, author_id)
