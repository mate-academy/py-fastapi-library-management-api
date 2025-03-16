from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from db import crud
from db.database import SessionLocal
from schemas import BookSchemaResponse, BookSchemaCreate, AuthorSchemaCreate, AuthorSchemaResponse

router = APIRouter()

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 3


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def root() -> dict:
    return {"FastApi library management project": "Version 1.0.0"}


@router.get("/books", response_model=List[BookSchemaResponse])
def get_books(
        db: Session = Depends(get_db),
        limit: int = Query(DEFAULT_PAGE, ge=0),
        offset: int = Query(DEFAULT_PAGE_SIZE, ge=0)
):
    return crud.get_books(db, offset=offset, limit=limit)


@router.get("/books/{book_id}", response_model=BookSchemaResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/books", response_model=BookSchemaResponse)
def create_book(book: BookSchemaCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=book.author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(book=book, db=db)


@router.post("/authors", response_model=AuthorSchemaResponse)
def create_author(author: AuthorSchemaCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(author=author, db=db)


@router.get("/authors/{author_id}", response_model=AuthorSchemaResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@router.get("/authors", response_model=List[AuthorSchemaResponse])
def get_authors(
        db: Session = Depends(get_db),
        limit: int = Query(DEFAULT_PAGE, ge=0),
        offset: int = Query(DEFAULT_PAGE_SIZE, ge=0),):
    return crud.get_authors(db, limit=limit, offset=offset)
