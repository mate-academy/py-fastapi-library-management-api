from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud
from . import schemas
from .db.engine import SessionLocal

from fastapi import FastAPI


app = FastAPI()


class DBSession:
    def __init__(self):
        self._session = None

    def __enter__(self):
        self._session = SessionLocal()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()

def get_db() -> Session:
    with DBSession() as db:
        yield db


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(db: Session = Depends(get_db)):
    return crud.get_all_author(db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
              author_id: int = None,
              db: Session = Depends(get_db)
):
    return crud.get_book_list(db=db,  author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
