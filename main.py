from sqlalchemy.orm import Session
import crud
from database import engine, SessionLocal
from models import Base
from schemas import AuthorCreate, AuthorResponse, BookResponse, BookCreate
from fastapi import FastAPI, Depends, HTTPException
from typing import List


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors", response_model=List[AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.post("/authors/{author_id}/books", response_model=BookResponse)
def create_book(author_id: int, book: BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.get("/books", response_model=List[BookResponse])
def read_books(skip: int = 0, limit: int = 100, author_id: int = None, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
