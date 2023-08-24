from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import add_pagination, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

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
    return {"message": "Greetings!"}


@app.get("/authors/", response_model=Page[schemas.Author])
def read_authors_list(db: Session = Depends(get_db)):
    return paginate(db, crud.get_all_authors(db=db))


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
    db_author = crud.get_authors_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with such name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def read_books_list(
    author_id: int | None = None,
    db: Session = Depends(get_db)
):
    return paginate(db, crud.get_book_list(db=db, author_id=author_id))


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
