from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud import (
    get_books,
    get_book_by_id,
    create_book,
    get_author,
    get_author_by_id,
    create_author,
)
from database import engine
from models import Base
from schemas import (
    BookList,
    BookDetail,
    BookCreate,
    AuthorList,
    AuthorDetail,
    AuthorCreate,
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/books", response_model=List[BookList])
def list_books(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_books(limit=limit, offset=offset, db=db)


@app.get("/books/{book_id}", response_model=BookDetail)
def detail_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(id=book_id, db=db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=BookDetail)
def post_books(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(book=book, db=db)


@app.get("/authors", response_model=List[AuthorList])
def list_authors(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_author(limit=limit, offset=offset, db=db)


@app.get("/authors/{author_id}", response_model=AuthorDetail)
def detail_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(id=author_id, db=db)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors", response_model=AuthorDetail)
def post_authors(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(author=author, db=db)
