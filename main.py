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


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/books/", response_model=list[schemas.BookList])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)


@app.post("/books/", response_model=schemas.BookRetrieve)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/{book_id}/", response_model=schemas.BookRetrieve)
def get_single_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_single_book(db, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/authors/", response_model=schemas.AuthorRetrieve)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRetrieve)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_single_author(db, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author
