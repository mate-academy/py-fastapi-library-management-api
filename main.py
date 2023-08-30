from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()

add_pagination(app)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=Page[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return paginate(crud.get_all_authors(db=db))


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author(author_id=author_id, db=db)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with such name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int | None = None
):
    return paginate(crud.get_all_books(db=db, author_id=author_id))


@app.get("/books/{book_id}/", response_model=schemas.Author)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(book_id=book_id, db=db)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)
