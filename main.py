from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session

import schemas
import models
import crud
from database import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


app = FastAPI()
add_pagination(app)


@app.get(
    "/authors/",
    response_model=Page[schemas.AuthorListRetrieveModel]
)
def get_all_authors(
    db: Session = Depends(get_db)
) -> Page[models.Author]:
    return paginate(crud.get_author_list(db))


@app.get(
    "/authors/{pk}/",
    response_model=schemas.AuthorListRetrieveModel
)
def get_single_author(
    pk: int,
    db: Session = Depends(get_db)
) -> models.Author:
    author = crud.get_author_by_id(db, pk)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author


@app.post("/authors/", response_model=schemas.AuthorListRetrieveModel)
def write_author(
    data: schemas.AuthorCreateModel,
    db: Session = Depends(get_db)
) -> models.Author:
    return crud.create_author(db, data)


@app.get("/books/", response_model=Page[schemas.BookListRetrieveModel])
def get_all_books(
    author_id: int | None = None,
    db: Session = Depends(get_db)
) -> Page[models.Book]:
    return paginate(crud.get_book_list(db, author_id))


@app.post("/books/", response_model=schemas.BookListRetrieveModel)
def write_book(
    data: schemas.BookCreateModel,
    db: Session = Depends(get_db)
) -> models.Book:
    return crud.create_book(db=db, data=data)
