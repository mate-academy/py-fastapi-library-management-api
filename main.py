from typing import List, Optional

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas

app = FastAPI()


def get_db() -> Session:
    db = Session()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    return crud.get_all_authors(db=db)[skip: skip + limit]


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
        author_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    return crud.books(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book_for_author(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
