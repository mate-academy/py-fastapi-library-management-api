from typing import Optional

from fastapi import Depends, Query, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors_paginated(
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_all_authors_paginated(db, page, size)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db, author.name):
        raise HTTPException(
            status_code=400, detail="An author with such a name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books_paginated(
    author_id: Optional[int] = None,
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_all_books_paginated(db, author_id, page, size)


@app.post("/books/", response_model=schemas.Book)
def create_book_for_author(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    if crud.get_book_by_title(db, book.title):
        raise HTTPException(
            status_code=400,
            detail="A book with such a title already exists"
        )
    if not crud.get_author_by_id(db, book.author_id):
        raise HTTPException(
            status_code=400,
            detail="The author with the specified id does not exist"
        )
    return crud.create_book_for_author(db=db, book=book)
