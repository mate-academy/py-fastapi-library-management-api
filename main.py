from fastapi import FastAPI, Depends, HTTPException
from typing import Generator, Annotated

from sqlalchemy.orm import Session
from database import SessionLocal

import schemas
from schemas import FilterParams
import crud

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World and Sasha"}

@app.get("/authors", response_model=list[schemas.AuthorRead])
def get_authors(filter_query: Annotated[FilterParams, Depends()], db: Session = Depends(get_db)):
    return crud.get_author_list(db=db, skip=filter_query.skip, limit=filter_query.limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)

@app.post("/authors", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=list[schemas.BookRead])
def get_books(filter_query: Annotated[FilterParams, Depends()], db: Session = Depends(get_db)):
    return crud.get_book_list(db=db, skip=filter_query.skip, limit=filter_query.limit)


@app.get("/books/{author_id}", response_model=list[schemas.BookRead])
def get_book_by_author_id(author_id: int, db: Session = Depends(get_db)):
    current_author = crud.get_author_by_id(db=db, author_id=author_id)

    if current_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    founded_book = crud.get_book_by_author_id(db=db, author_id=current_author.id)

    if founded_book is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return founded_book

@app.post("/books", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
