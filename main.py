from sqlalchemy.orm import Session
from models import Base

import crud
import schemas

from fastapi import FastAPI, Depends, HTTPException

from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return crud.get_all_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    author_db = crud.get_author(db=db, author_id=author_id)
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_db

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )

@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    db_author = crud.get_author(db=db, author_id=book.author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)
