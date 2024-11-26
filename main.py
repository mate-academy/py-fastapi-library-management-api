from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import (get_authors, get_author_by_id, create_author,
                  create_book, get_books, get_books_by_author)
from database import SessionLocal, engine
from models import Base
from schemas import AuthorCreate, BookCreate, Author, Book


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=Author)
def create_author_view(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db=db, author=author)


@app.get("/authors", response_model=list[Author])
def get_authors_view(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def get_author_view(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books", response_model=Book)
def create_book_view(book: BookCreate, db: Session = Depends(get_db)):
    db_author = get_author_by_id(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author id not exist")
    return create_book(db=db, book=book, author_id=book.author_id)


@app.get("/books", response_model=list[Book])
def get_books_view(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db=db, skip=skip, limit=limit)


@app.get("/books/author/{author_id}", response_model=list[Book])
def get_books_by_author_view(author_id: int, db: Session = Depends(get_db)):
    db_books = get_books_by_author(db=db, author_id=author_id)
    if not db_books:
        raise HTTPException(status_code=404, detail="Books not found for this author")
    return db_books
