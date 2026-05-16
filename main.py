from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud
from database import SessionLocal, Base, engine
from schemas import AuthorRead, AuthorCreate, BookCreate, BookRead

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}

@app.post("/authors/", response_model=AuthorRead)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[AuthorRead])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id=author_id)

@app.post("/books/", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book=book)

@app.get("/books/", response_model=List[BookRead])
def read_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        author_id: int = None,
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
