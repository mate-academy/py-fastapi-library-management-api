from typing import Optional

from fastapi import FastAPI, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.params import Depends

import crud
import schemas


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.post("/author/", response_model=schemas.AuthorCreate)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists."
        )

    return crud.create_new_author(db=db, author=author)


@app.get("/author/", response_model=list[schemas.Author])
def get_author_list(
        skip: int,
        limit: int,
        db: Session = Depends(get_db),
):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post("/book/", response_model=schemas.BookCreate)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_new_book(db=db, book=book)


@app.get("/book/", response_model=list[schemas.Book])
def get_book_list(
        author_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
):
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.get("/book/{book_id}", response_model=schemas.Book)
def get_book_by_id(
        book_id: int,
        db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return db_book
