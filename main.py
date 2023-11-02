from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int = None,
        skip: int = 0,
        limit: int = 100
):
    return crud.get_all_books(db=db, author_id=author_id)[skip: skip + limit]


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book is not found")

    return crud.get_book_by_id(db, book_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return crud.get_all_authors(db=db)[skip: skip + limit]


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author is not found")

    return db_author
