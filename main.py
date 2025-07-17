from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Optional

import schemas
import crud
import models
app = FastAPI()


@app.get("/")
def hello():
    return "Hello!"


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/authors/", response_model=list[schemas.AuthorList])
def get_list_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(2, ge=1, le=2),
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)

@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(models.Author).filter(models.Author.name == author.name).first()

    if existing_author:
        raise HTTPException(status_code=400, detail="This Author already exist")

    author = crud.create_author(author=author, db=db)
    return author

@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(book=book, db=db)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.get("/books/", response_model=list[schemas.BookList])
def get_list_books(
        author_id: Optional[int] = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(2, ge=1, le=2),
        db: Session = Depends(get_db)):
    return crud.get_all_books(author_id=author_id, skip=skip, limit=limit, db=db)
