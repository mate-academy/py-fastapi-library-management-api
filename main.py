from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing_extensions import Annotated

import crud
import models
import schemas
from database import SessionLocal, engine
from schemas import AuthorRead, BookRead

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[AuthorRead])
def read_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(
        new_author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=new_author.name)

    if db_author:
        raise HTTPException(status_code=400,
                            detail="author name already exist")

    return crud.create_author(db=db, author=new_author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_single_author(
        author_id: int,
        db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=List[BookRead])
def read_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books", response_model=List[BookRead])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author_id(db, author_id)
    if not books:
        raise HTTPException(status_code=404,
                            detail="No books found for this author")
    return books


@app.post("/authors/{author_id}/books", response_model=BookRead)
def create_book(author_id: int, book: schemas.BookCreate,
                db: Session = Depends(get_db)):
    new_book = crud.create_book_for_author(db, author_id, book)
    if not new_book:
        raise HTTPException(status_code=404, detail="Author not found")
    return new_book
