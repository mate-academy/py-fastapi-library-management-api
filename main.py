from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

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
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(
    skip: int | None = None,
    limit: int | None = None,
    db: Session = Depends(get_db),
) -> List[schemas.Author]:
    return crud.get_all_author(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404, detail=f"Author with id: {author_id} not found"
        )
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
    skip: int | None = None,
    limit: int | None = None,
    author_id: int | None = None,
    db: Session = Depends(get_db),
) -> List[schemas.Book]:
    return crud.get_all_book(
        db=db, skip=skip, limit=limit, author_id=author_id
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)
