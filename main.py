from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root() -> dict:
    return {"message": "Hello"}

@app.get("/authors/", response_model=list[schemas.AuthorBase])
def read_author(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)

@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(
        author: schemas.AuthorBase,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=list[schemas.BookBase])
def read_book(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)

@app.post("/books/", response_model=schemas.BookBase)
def create_book(
        book: schemas.BookBase,
        db: Session = Depends(get_db),
):
    db_book = crud.create_book(db=db, book=book)

    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    return crud.create_book(db=db, book=book)
