from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorSCH)
def create_author(
        author: schemas.AuthorSCHCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.AuthorSCH])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorSCH)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.get("/books/", response_model=list[schemas.BookSCH])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookSCH)
def create_book(
        book: schemas.BookSCHCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)


@app.get("/books/by_author/{author_id}", response_model=list[schemas.BookSCH])
def get_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_author_id(db=db, author_id=author_id)
