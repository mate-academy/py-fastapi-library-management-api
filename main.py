from typing import Generator, List, Annotated

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException


import crud
import models
import schemas
from database import SessionLocal


app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors", response_model=list[schemas.Author])
def get_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100
) -> List[models.DBAuthor]:
    return crud.retrieve_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author(
    db: Annotated[Session, Depends(get_db)],
    author_id: int
) -> models.DBAuthor | None:
    return crud.retrieve_author_by_id(db=db, author_id=author_id)


@app.get("/books", response_model=list[schemas.Book])
def get_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100
) -> List[models.DBBook]:
    return crud.retrieve_books(db=db, skip=skip, limit=limit)


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)]
) -> models.DBAuthor:

    existing_author = crud.get_author_by_name(db=db, name=author.name)
    if existing_author is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Author with name '{author.name}' already exists"
        )

    return crud.create_author(db=db, author=author)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> models.DBBook:

    if not crud.is_author_exists(db=db, author_id=book.author_id):
        raise HTTPException(
            status_code=400,
            detail=f"Author with id '{book.author_id}' does not exist"
        )

    return crud.create_book(db=db, book=book)


@app.post("/books", response_model=list[schemas.Book])
def get_books_by_author_id(
    db: Annotated[Session, Depends(get_db)],
    author_id: int
) -> list[models.DBBook] | None:

    if not crud.is_author_exists(db=db, author_id=author_id):
        raise HTTPException(
            status_code=400,
            detail=f"Author with id '{author_id}' does not exist"
        )

    return crud.retrieve_books_by_author_id(db=db, author_id=author_id)
