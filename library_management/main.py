from typing import List

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from crud import create_author, get_authors, get_author, create_book, get_books, get_books_by_author
from schemas import AuthorCreate, Author, AuthorList, BookCreate, Book

app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_new_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)


@app.get("/authors/", response_model=AuthorList)
def list_authors(skip: int = Query(0), limit: int = Query(10), db: Session = Depends(get_db)):
    authors = get_authors(db, skip, limit)
    return {"items": authors}


@app.get("/authors/{author_id}", response_model=Author)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=Book)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)


@app.get("/books/", response_model=List[Book])
def list_books(skip: int = Query(0), limit: int = Query(10), db: Session = Depends(get_db)):
    return get_books(db, skip, limit)


@app.get("/books/by_author/{author_id}", response_model=List[Book])
def list_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return get_books_by_author(db, author_id)


if __name__ == "__main__":
    uvicorn.run(
        "library_management.main:app", port=8000, reload=True
    )
