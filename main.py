from datetime import date

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[Author])
def read_authors(
        db: Session = Depends(get_db),
        author_id: int = None,
        limit: int = 10,
        offset: int = 0
):
    return crud.get_authors_list(db, author_id=author_id, limit=limit, offset=offset)


@app.post("/authors/create/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/update/", response_model=Author)
def update_author(
        author_id: int,
        name: str = None,
        bio: str = None,
        db: Session = Depends(get_db)
):
    return crud.update_author(db=db, author_id=author_id, name=name, bio=bio)


@app.delete("/authors/{author_id}/delete/", response_model=Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(db=db, author_id=author_id)


@app.get("/books/", response_model=list[Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int = None,
        limit: int = 10,
        offset: int = 0
):
    return crud.get_books_list(db, author_id=author_id, limit=limit, offset=offset)


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/create/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.post("/books/{book_id}/update/", response_model=Book)
def update_book(
        book_id: int,
        title: str = None,
        summary: str = None,
        publication_date: date = None,
        author_id: int = None,
        db: Session = Depends(get_db)
):
    return crud.update_book(
        db=db,
        book_id=book_id,
        title=title,
        summary=summary,
        publication_date=publication_date,
        author_id=author_id
    )


@app.delete("/books/{book_id}/delete/", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db=db, book_id=book_id)
