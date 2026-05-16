from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException, Query

import crud
import schemas
from database import base, engine, SessionLocal

app = FastAPI()


base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorList])
def authors_list(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=9, ge=1),
    db: Session = Depends(get_db)
    ):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def author_detail(
    author_id: int,
    db: Session = Depends(get_db)
    ):
    author = crud.get_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author with this id is not found")

    return author


@app.post("/authors/", response_model=schemas.AuthorList)
def author_create(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookList])
def books_list(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=9, ge=1),
        author_id: int | None = None,
        db: Session = Depends(get_db)
    ):
    return crud.get_all_books(skip=skip, limit=limit, db=db, author_id=author_id)


@app.get("/books/{book_id}/", response_model=schemas.BookList)
def book_detail(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book with this id is not found")

    return book


@app.post("/books/", response_model=schemas.BookList)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
