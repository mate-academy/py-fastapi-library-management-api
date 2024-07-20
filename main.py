from fastapi import Depends, FastAPI, HTTPException

import schemas
import crud
from sqlalchemy.orm import Session
from db.database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/library/books/skip={skip}&limit={limit}",
         response_model=list[schemas.BookSchema])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_books(db, skip, limit)


@app.get("/library/authors/skip={skip}&limit={limit}",
         response_model=list[schemas.AuthorSchema])
def get_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_authors(db, skip, limit)


@app.get("/library/authors/{author_id}", response_model=schemas.AuthorSchema)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id)


@app.get("/library/books/{author_id}", response_model=list[schemas.BookSchema])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(db, author_id)


@app.post("/library/books", response_model=schemas.BookCreateSchema)
def create_book(book: schemas.BookCreateSchema, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.post("/library/authors", response_model=schemas.AuthorCreateSchema)
def create_author(author: schemas.AuthorCreateSchema,
                  db: Session = Depends(get_db)):
    if crud.get_author_by_name(db, name=author.name):
        raise HTTPException(status_code=400,
                            detail="Author with this name already exists")
    return crud.create_author(db, author)
