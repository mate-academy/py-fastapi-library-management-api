from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
import schemas


app = FastAPI()


def get_db():
    db = SessionLocal()
    yield db
    db.close()


@app.get("/")
def hello_world():
    return "Hello World!!!"


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    author_id: int | None = None,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
):
    return crud.get_all_books(db, page=page, author_id=author_id)


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    if crud.get_book_by_title(db=db, title=book.title):
        raise HTTPException(400, "Such book alredy exists")    

    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book_details(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = crud.get_book_by_id(db=db, id=book_id)

    if not book:
        raise HTTPException(400, "No book with such id")

    return book


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
):
    return crud.get_all_authors(db, page=page)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author_by_name(db=db, name=author.name):
        raise HTTPException(400, "Such author alredy exists")

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_details(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db=db, id=author_id)

    if not author:
        raise HTTPException(400, "No author with such id")

    return author
