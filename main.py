from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db import schemas, crud
from db.database import Base, SessionLocal, engine
from db import models

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    author_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_book_list_by_author(
        db, author_id=author_id, skip=skip, limit=limit
    )

@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):

    db_author = crud.get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author_by_id(db, author_id=book.author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)
