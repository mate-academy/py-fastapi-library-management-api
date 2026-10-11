from fastapi import FastAPI, Depends, HTTPException
from collections.abc import Generator
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

import crud
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"msg": "Welcome to the library"}

@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def get_authors(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)):
    return crud.get_authors_list(db, skip, limit)
    

@app.get("/authors/{id}", response_model=schemas.AuthorResponse)
def get_author_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    existing_id = crud.get_author_by_id(db, id)

    if existing_id is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return crud.get_author_by_id(db, id)

@app.post("/authors/", response_model=schemas.AuthorResponse)
def add_author(
    author: schemas.AddAuthor,
    db: Session = Depends(get_db)
):
    existing_author = crud.get_author_by_name(db, author.name)

    if existing_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )

    
    result = crud.add_author(db, author)
    return result
    

@app.get("/books/", response_model=list[schemas.BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)):
    return crud.get_books_list(db, skip, limit)

@app.get("/books/{author_id}", response_model=list[schemas.BookResponse])
def get_books_by_author_id(
    author_id: int,
    db: Session = Depends(get_db)
):

    existing_author_by_id = crud.get_author_by_id(db, author_id)
    
    if existing_author_by_id is None:
        raise HTTPException(
            status_code=404,
            detail="Author with such id does not exist"
        )
    
    result = crud.get_books_by_author_id(db, author_id)
    return result

@app.post("/books/", response_model=schemas.BookResponse)
def add_book(
    book: schemas.AddBook,
    db: Session = Depends(get_db)
):
    result = crud.add_book(db, book)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return result
