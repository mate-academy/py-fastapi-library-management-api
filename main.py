from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db_library.engine import SessionLocal

import crud
import schemas

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/author/", response_model=list[schemas.Author])
def get_author_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return crud.get_all_authors(db=db, limit=limit, skip=skip)


@app.get("/author/{author_id}/")
def get_author_id(
        author: int,
        db: Session = Depends(get_db),
):
    return crud.get_author_by_id(db=db, author=author)


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def get_author_all(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return crud.get_all_book_paginate(db=db, limit=limit, skip=skip)


@app.post("/book/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)


@app.get("/book/{author_id}/")
def get_author_id(
        author: int,
        db: Session = Depends(get_db),
):
    return crud.get_book_on_author(db=db, author=author)
