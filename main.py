from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import schemas, crud
from database import SessionLocal


app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        db_author = crud.create_author(db, author)
        return db_author
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Author with this name already exists")


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = crud.create_book_for_author(db, author_id, book)
    return db_book


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(skip: int = 0, limit: int = 10, author_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
