from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db, author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book(
    author_id: int,
    book: schemas.BookBase,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    book_data = schemas.BookCreate(
        **book.model_dump(),
        author_id=author_id
    )

    return crud.create_book(db=db, book=book_data)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return crud.get_books_by_author(db, author_id)
