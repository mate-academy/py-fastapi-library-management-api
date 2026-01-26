from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db=db, name=author.name):
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exist"
        )
    return crud.create_author(db=db, author=author)

@app.get("/authors/skip={skip},limit={limit}", response_model=list[schemas.Author])
def read_authors(skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db=db, author_id=author_id)

@app.get("/books/skip={skip},limit={limit}", response_model=list[schemas.Book])
def read_books(skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)

@app.get("/books/{author_id}", response_model=list[schemas.Book])
def read_books_with_current_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books(db=db, author_id=author_id)

@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)