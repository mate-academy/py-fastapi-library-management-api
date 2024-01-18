from typing import Any

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate

import schemas
from db.database import SessionLocal
import crud

app = FastAPI()
add_pagination(app)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=LimitOffsetPage[schemas.Author])
def get_authors(db: Session = Depends(get_db)) -> Any:
    return paginate(crud.get_author_list(db))


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_specific_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="There are no authors with this ID")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author_data: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author_data)


@app.get("/books/", response_model=LimitOffsetPage[schemas.Book])
def get_books(author_id: int | None = None, db: Session = Depends(get_db)):
    return paginate(crud.get_book_list(db=db, author_id=author_id))


@app.post("/authors/{author_id}/books/", response_model=schemas.BookCreate)
def create_book_for_a_specific_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book_for_a_specific_author(db=db, author_id=author_id, book=book)
