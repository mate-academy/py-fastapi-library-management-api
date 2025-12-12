from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authors
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Author).filter(models.Author.name == author.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

# Books
@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
