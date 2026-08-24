from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from database import SessionLocal, engine
from typing import Generator, Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author_endpoint(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        return db_author

@app.post("/authors/{author_id}/books/", response_model=schemas.BookResponse)
def create_book_for_author(book: schemas.BookCreate, author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = crud.create_book(db=db, book=book, author_id=author_id)
    return new_book

@app.get("/books/", response_model=list[schemas.BookResponse])
def read_books_endpoint(author_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, author_id=author_id, skip=skip, limit=limit)
    return books
