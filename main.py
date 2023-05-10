from fastapi import FastAPI, Depends, HTTPException

from fastapi_pagination import Page, add_pagination, LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session
from sqlalchemy import select

import schemas
import crud
from db.engine import SessionLocal
import db.models as models


app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello, world!"}


@app.get("/authors/", response_model=LimitOffsetPage[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return paginate(db, select(models.DBAuthor).order_by(models.DBAuthor.name))


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 50,
        title: str | None = None,
        summary: str | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_book_list(db=db, skip=skip, limit=limit, title=title, summary=summary)


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Such book already exists"
        )

    return crud.create_book(db=db, book=book)

add_pagination(app)
