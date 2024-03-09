from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

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


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def list_author(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    return crud.authors(db=db)[skip: skip + limit]


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    return crud.author(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book_for_author(
        book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(book=book, db=db)


@app.get("/books/", response_model=List[schemas.Book])
def list_books(
        author_id: Optional[int] = None, db: Session = Depends(get_db)
):
    return crud.books(db=db, author_id=author_id)
