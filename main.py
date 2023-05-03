from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from db.database import SessionLocal
import schemas

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db)
    return authors[skip: skip + limit]


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=list[schemas.Book])
def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_all_books(db=db)
    return books[skip: skip + limit]


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def get_books_by_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    books = crud.get_books_by_author(db, author_id)
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)
