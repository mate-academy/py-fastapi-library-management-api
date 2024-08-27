from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db import models
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)) -> list[schemas.Author]:
    return crud.get_all_authors(db=db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already registered"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db)) -> list[schemas.Book]:
    return crud.get_all_books(db=db)


@app.post("/books/{author_id}/", response_model=schemas.Book)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(
        db=db,
        book=book,
        author_id=author_id
    )


@app.get(
    "/books/author/{author_id}",
    response_model=list[schemas.Book]
)
def read_books_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_books_by_author_id(
        db=db,
        author_id=author_id
    )
