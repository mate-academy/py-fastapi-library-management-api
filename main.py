from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import AuthorList, BookList
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


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> AuthorList:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorList])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> List[AuthorList]:
    authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> AuthorList:
    db_author = crud.get_author(db=db, authors_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookList)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> BookList:
    db_book = crud.get_book_by_author_id(
        db=db,
        author_id=author_id
    )

    if db_book:
        raise HTTPException(status_code=400, detail="Book not found")
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.BookList])
def read_all_books(
        db: Session = Depends(get_db),
        limit: int | None = None,
        skip: int | None = None,
) -> List[BookList]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list[schemas.BookList])
def read_books_by_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> List[BookList]:
    books = crud.get_book_by_author_id(db=db, author_id=author_id)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this author")
    return books
