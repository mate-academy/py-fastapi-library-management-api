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


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author:
        return db_author

    raise HTTPException(status_code=404, detail="Author not found")


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_author_book(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_all_books(db=db, skip=skip, limit=limit)
    return books


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id)
    return books
