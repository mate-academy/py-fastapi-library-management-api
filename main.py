from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.AuthorCreate])
def read_authors(db: Annotated[Session, Depends(get_db)]):
    return crud.get_all_authors(db)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_single_author(
        author_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookList])
def read_book(
        db: Annotated[Session, Depends(get_db)],
        author_id: str | None = None,
):
    return crud.get_book_list(
        db=db, author_id=author_id
    )


@app.get("/books/{book_id}/", response_model=schemas.BookList)
def get_single_book(
        book_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=schemas.BookList)
def create_book(
        book: schemas.BookCreate,
        db: Annotated[Session, Depends(get_db)]
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this title already exist")

    author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not author:
        raise HTTPException(status_code=400, detail="Author not found")

    return crud.create_book(db=db, book=book)
