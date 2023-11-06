from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = Query(default=0),
        limit: int = Query(default=10),
        db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = Query(default=0),
        limit: int = Query(default=10),
        db: Session = Depends(get_db)):
    books = crud.get_all_books(db=db, skip=skip, limit=limit)
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/author/{author_id}/", response_model=schemas.Book)
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_books_by_author_id(db=db, author_id=author_id)
    return db_book

