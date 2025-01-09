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


@app.get("/authors/", response_model=list[schemas.AuthorSchema])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_all_author(db=db, skip=0, limit=5)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorSchema)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.retrieve_author(db=db, author_id=author_id)


@app.post("/authors/", response_model=schemas.AuthorSchema)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookSchema])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=0, limit=5)


@app.get("/books/{author_id}", response_model=list[schemas.BookSchema])
def get_book(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=0, limit=5, author_id=author_id)


@app.post("/books/", response_model=schemas.BookSchema)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
