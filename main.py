from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Type

import crud
import schemas
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Catalog API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.post("/create_author/", response_model=schemas.AuthorList)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
) -> models.DBAuthor:
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorList])
def read_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> list[Type[models.DBAuthor]]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorList)
def read_author(
    author_id: int,
    db: Session = Depends(get_db)
) -> models.DBAuthor:
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/create_book/", response_model=schemas.BookList)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> list[Type[models.DBBook]]:
    author = crud.get_author_by_id(db, book.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.BookList])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> list[Type[models.DBBook]]:
    return crud.get_all_books(db, skip, limit, author_id)
