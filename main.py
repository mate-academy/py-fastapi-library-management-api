from typing import List

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


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def post_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_authors_by_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def post_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/author/{author_id}/", response_model=List[schemas.Book])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db=db, author_id=author_id)
