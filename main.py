from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal
from schemas import BookBase

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}

@app.get("/books/", response_model=list[schemas.Book])
def books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_books(db, skip, limit)

@app.get("/book/{id}", response_model=schemas.Book)
def book(id: int, db: Session = Depends(get_db)) -> schemas.Book:
    return crud.get_book_by_id(db, id)

@app.post("/book/", response_model=schemas.Book)
def create_book(
        book_data: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db, book_data)

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author_data: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    return crud.create_author(db, author_data)

@app.get("/authors/", response_model=schemas.Author)
def authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_authors(db, skip, limit)

@app.get("/author/{id}/", response_model=schemas.Author)
def get_author(id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, id)

@app.get("/author/{id}/books/", response_model=list[schemas.Book])
def get_book_by_author(id: int, db: Session = Depends(get_db)):
    return crud.filter_books_by_author(db, id)

