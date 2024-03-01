from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/author/{author_id}", response_model=List[schemas.Book])
def read_books_by_author(author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    return books
