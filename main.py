from typing import Generator, List, Annotated

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import crud
import models
import schemas
from database import engine, SessionLocal


class AuthorNotExist(HTTPException):
    def __init__(
        self,
        author_id: int
    ):
        super().__init__(
            status_code=400,
            detail=f"Author with id '{author_id}' does not exist"
        )


class AuthorAlreadyExists(HTTPException):
    def __init__(
        self,
        author_index: str
    ):
        super().__init__(
            status_code=400,
            detail=f"Author with index '{author_index}' already exists"
        )


models.Base.metadata.create_all(bind=engine)


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


@app.post("/book/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> models.DBBook:

    if not crud.retrieve_author_by_id(db=db, author_id=book.author_id):
        raise AuthorNotExist(author_id=book.author_id)

    return crud.create_book(db=db, book=book)


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)]
) -> models.DBAuthor:

    if crud.get_author_by_name(db=db, name=author.name):
        raise AuthorAlreadyExists(author_index=author.name)

    return crud.create_author(db=db, author=author)


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
) -> models.DBAuthor:

    author = crud.retrieve_author_by_id(db=db, author_id=author_id)

    if not author:
        raise AuthorNotExist(author_id=author_id)

    return author


@app.get("/books", response_model=list[schemas.Book])
def get_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None
) -> list[models.DBBook]:

    if (
        author_id and not crud.retrieve_author_by_id(
            db=db,
            author_id=author_id)
    ):
        raise AuthorNotExist(author_id=author_id)

    return crud.retrieve_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )
