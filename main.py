from typing import List

from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import BookResponse, BookBase

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)


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
