from datetime import date

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    book: str | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, book=book, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_single_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="No author with this id")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    publication_date: date | None = None,
    author: str | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_book_list(
        db=db,
        publication_date=publication_date,
        author=author,
        skip=skip,
        limit=limit
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="No book with this id")
    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
