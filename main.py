from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
import crud
from database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    if not crud.get_author(db, author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if author_id is not None:
        return crud.get_books_by_author(db, author_id, skip, limit)
    return crud.get_books(db, skip, limit)
