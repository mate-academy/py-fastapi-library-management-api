from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import BookResponse, BookBase, AuthorBase, AuthorResponse

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=List[BookResponse])
def get_books(
        author_id: int | None = None,
        db: Session = Depends(get_db)):
    return crud.get_all_books(db=db, author_id=author_id)


@app.get("/books/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db=db, id=id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/", response_model=BookResponse)
def create_book(book: BookBase, db: Session = Depends(get_db)):
    return crud.create_book(
        db=db,
        data=book,
    )


@app.get("/authors/", response_model=List[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db=db)


@app.get("/authors/{id}", response_model=AuthorResponse)
def get_author(id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, id=id)
    if author:
        return author
    else:
        raise HTTPException(status_code=404, detail="Author not found")


@app.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorBase, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db=db, name=author.name):
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(
        db=db,
        data=author,
    )
