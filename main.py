from fastapi import FastAPI, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session

from crud import (
    get_authors_list,
    get_author,
    create_author,
    get_books_list,
    get_book,
    create_book,
)
from database import SessionLocal, engine
from models import Base
from schemas import AuthorSchema, AuthorCreate, BookSchema, BookCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[AuthorSchema])
def read_authors_list(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
):
    return get_authors_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=AuthorSchema)
def read_author(author_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_author = get_author(author_id=author_id, db=db)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=AuthorSchema, status_code=201)
def add_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = create_author(author=author, db=db)
    if db_author is None:
        raise HTTPException(status_code=409, detail="Author name already exists")

    return db_author


@app.get("/books/", response_model=list[BookSchema])
def read_books_list(
    db: Session = Depends(get_db),
    author_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, gt=0),
):
    return get_books_list(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=BookSchema)
def read_book(book_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_book = get_book(book_id=book_id, db=db)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=BookSchema, status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = create_book(book=book, db=db)

    if db_book is None:
        raise HTTPException(
            status_code=404, detail=f"Author with id {book.author_id} not found"
        )

    return db_book
