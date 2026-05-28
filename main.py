from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate,
                  db: Session = Depends(get_db)) -> models.Author:
    return crud.create_author(db=db, author=author)


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip: int = 0,
                 limit: int = 100) -> list[models.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int,
                db: Session = Depends(get_db)) -> models.Author:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books", response_model=schemas.Book)
def create_book(author_id: int, book: schemas.BookCreate,
                db: Session = Depends(get_db)) -> models.Book:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, author_id=author_id, book=book)


@app.get("/books", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db), skip: int = 0,
               limit: int = 100) -> list[models.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)) -> \
        list[models.Book]:
    return crud.get_books_by_author(db=db, author_id=author_id)
