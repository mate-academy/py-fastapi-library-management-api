from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import paginate, Page, add_pagination
from sqlalchemy.orm import Session

import crud
from db.database import SessionLocal
from schemas import Book, BookCreate, AuthorCreate, Author

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


@app.get("/books/", response_model=List[Book])
def read_books(db: Session = Depends(get_db),
               skip: int = 0,
               limit: int = 10):
    return crud.get_all_books(db, skip, limit)


@app.get("/books/{author_id}/", response_model=List[Book])
def read_books_by_author_id(author_id: int,
                            db: Session = Depends(get_db),
                            skip: int = 0,
                            limit: int = 10):
    db_books = crud.get_books_by_author_id(db,
                                           author_id,
                                           skip,
                                           limit)

    if not db_books:
        raise HTTPException(status_code=404, detail="Books not found")
    return paginate(db_books)


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate,
                db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=List[Author])
def read_authors(db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 10):
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate,
                  db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)
