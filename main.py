from collections.abc import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

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


@app.get("/authors/", response_model=list[schemas.AuthorList])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def get_one_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author does not exist"
        )
    return author


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.scalar(select(models.Author).where(models.Author.name == author.name))
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exist"
        )
    return crud.create_author(
        db=db,
        author=author,
    )


@app.get("/books/", response_model=list[schemas.BookList])
def get_all_books(db: Session = Depends(get_db), author_id: int | None = None):
    return crud.get_all_books(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.BookList)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = db.scalar(select(models.Author).where(models.Author.id == book.author_id))
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author does not exist"
        )
    return crud.create_book(db=db, book=book)
