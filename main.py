from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

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


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_authors(db)[skip: skip + limit]


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db, author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int = None,
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_books(db, author_id=author_id)[skip: skip + limit]


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db, book)
