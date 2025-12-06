from typing import List
from datetime import date
from database import Base, engine

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import (
    Author,
    AuthorCreate,
    AuthorUpdate,
    Book,
    BookCreate,
    BookUpdate,
)
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[Author])
def read_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}", response_model=Author)
def put_author(
        author: AuthorUpdate,
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.update_author(db=db, author_id=author_id, data=author)


@app.patch("/authors/{author_id}", response_model=Author)
def patch_author(
        author: AuthorUpdate,
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.update_author(db=db, author_id=author_id, data=author)


@app.delete("/authors/{author_id}", response_model=Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(db=db, author_id=author_id)


@app.get("/books/", response_model=List[Book])
def read_books(
        title: str | None = None,
        publication_date: date | None = None,
        author: int | None = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        db: Session = Depends(get_db)
):
    return crud.get_books_list(
        title=title,
        publication_date=publication_date,
        author=author,
        db=db,
        skip=skip,
        limit=limit
    )


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db=db, book_id=book_id)


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.put("/books/{book_id}", response_model=Book)
def put_book(
        book: BookUpdate,
        book_id: int,
        db: Session = Depends(get_db)
):
    return crud.update_book(db=db, book_id=book_id, data=book)


@app.patch("/books/{book_id}", response_model=Book)
def patch_book(
        book: BookUpdate,
        book_id: int,
        db: Session = Depends(get_db)
):
    return crud.update_book(db=db, book_id=book_id, data=book)


@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db=db, book_id=book_id)
