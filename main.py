from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorBase])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=list[schemas.Author])
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=schemas.BookBase)
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db, author)


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db, book)


@app.get("/books/by_author/{author_id}/", response_model=schemas.Book)
def read_book_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id)
    if not books:
        raise HTTPException(status_code=404, detail="Author not found")
    return books
