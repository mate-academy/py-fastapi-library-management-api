from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, SessionLocal, engine

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book, status_code=201)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_books(db, skip=skip, limit=limit, author_id=author_id)