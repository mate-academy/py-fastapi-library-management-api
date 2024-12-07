from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_cheese_type = crud.get_author_by_name(db=db, name=author.name)

    if db_cheese_type:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def list_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def list_books(
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    db_book = crud.get_books(db, author_id=author_id, skip=skip, limit=limit)
    if not db_book:
        raise HTTPException(status_code=404, detail="Such Books not found")

    return db_book
