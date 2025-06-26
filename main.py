from fastapi import FastAPI, Depends, HTTPException

import crud
from database import SessionLocal
from shemas import Author, AuthorCreate, BookCreate, Book
from sqlalchemy.orm import Session
app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=list[Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        author_id: int = None,
):
    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)