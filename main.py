from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


from db.database import SessionLocal

import crud
import schemas

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.BookList)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.BookList:
    existing_book = crud.get_book_by_title(db=db, title=book.title)

    if existing_book:
        raise HTTPException(
            status_code=400, detail="Such name for book already exists"
        )
    return crud.create_book(db=db, book=book)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.BookList])
def read_books(
        skip: int = 0,
        limit: int = 3,
        db: Session = Depends(get_db)
) -> List[schemas.BookList]:
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=List[schemas.BookList])
def read_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author_id(db, author_id=author_id)
    if not books:
        raise HTTPException(
            status_code=404, detail="No books found for this author"
        )
    return books


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 2, db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
