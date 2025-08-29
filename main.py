from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
from db.database import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED
)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):

    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_author_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    if author_id:
        books = crud.get_books_by_author(db=db, author_id=author_id, skip=skip, limit=limit)
    else:
        books = crud.get_books(db=db, skip=skip, limit=limit)
    return books


@app.get("/authors/{author_id}/books/", response_model=List[schemas.Book])
def read_books_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получает все книги определенного автора.
    """
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    books = crud.get_books_by_author(db=db, author_id=author_id, skip=skip, limit=limit)
    return books