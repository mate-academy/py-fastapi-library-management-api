from typing import Annotated, Generator

from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import add_pagination, Page
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine

app = FastAPI()
add_pagination(app)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=Page[schemas.Author])
def read_authors(db: Annotated[Session, Depends(get_db)]):
    return crud.get_all_authors(db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int, db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Book is not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author is already exists")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def read_book(
    db: Annotated[Session, Depends(get_db)],
    author_id: int | None = None,
):
    return crud.get_book_list(db=db, author_id=author_id)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Annotated[Session, Depends(get_db)]):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book is not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, db: Annotated[Session, Depends(get_db)]
):

    author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")

    return crud.create_book(db=db, book=book)
