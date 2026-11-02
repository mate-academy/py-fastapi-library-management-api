from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.post("/books/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)
