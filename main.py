from typing import List

import models
import schemas
import crud
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=List[schemas.Author])
def authors(db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    return crud.get_author_list(db=db, offset=offset, limit=limit)

@app.post("/authors", response_model=schemas.Author)
def author_create(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_new_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db=db, author_id=author_id)


@app.get("/books", response_model=List[schemas.Book])
def books(db: Session = Depends(get_db), offset: int = 0, limit: int = 100, author_id: int = None):
    return crud.get_book_list(db=db, offset=offset, limit=limit, author_id=author_id)


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_new_book(db=db, book=book)