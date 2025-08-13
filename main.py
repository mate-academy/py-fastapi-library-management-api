from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Query

import crud
import schemas
from database.engine import SessionLocal, engine, Base

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=List[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db),
):
    return crud.get_author_by_id(author_id=author_id, db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=List[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = Query(None, description="Filter books by author ID")
):
    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_book_by_id(book_id=book_id, db=db)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(book=book, db=db)
