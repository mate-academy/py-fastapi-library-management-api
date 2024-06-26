from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import SessionLocal
from schemas import AuthorList, AuthorCreate, BookList, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=List[AuthorList])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=AuthorList)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=AuthorList)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[BookList])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/author/{author_id}", response_model=List[BookList])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    books = crud.get_books_by_author_id(db, author_id=author_id, skip=skip, limit=limit)
    if not books:
        raise HTTPException(status_code=404, detail="Books not found for this author")
    return books


@app.post("/books/", response_model=BookList)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
