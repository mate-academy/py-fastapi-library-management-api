from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import (
    BookResponse,
    BookBase,
    AuthorBase,
    AuthorResponse,
    PaginatedBooks,
    PaginatedAuthors,
)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=PaginatedBooks)
def get_books(
    author_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    data = crud.get_all_books(db=db, author_id=author_id, offset=skip, limit=limit)
    total = crud.get_total_books(db)
    return {
        "skip": skip,
        "limit": limit,
        "total": total,
        "data": data,
    }


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


@app.get("/authors/", response_model=PaginatedAuthors)
def get_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    data = crud.get_authors(db=db, offset=skip, limit=limit)
    total = crud.get_total_authors(db)
    return {
        "skip": skip,
        "limit": limit,
        "total": total,
        "data": data,
    }


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
