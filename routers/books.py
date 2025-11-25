from schemas import schemas_books

from typing import Optional

from sqlalchemy.orm import Session

from crud import crud_books

from fastapi import Depends, HTTPException, APIRouter

from session_db import db_session


router = APIRouter()


@router.get("/books/", response_model=list[schemas_books.GetBooks])
def get_books_all(skip: int = 0, limit: int = 10, author_id: Optional[int] = None, db: Session = Depends(db_session)):
    return crud_books.get_books(db, skip=skip, limit=limit, author_id = author_id)


@router.get("/books/{book_id}", response_model=schemas_books.GetBooks)
def get_books_id(book_id: int, db: Session = Depends(db_session)):
    return crud_books.get_books_id(db, book_id)


@router.post("/books/", response_model=schemas_books.GetBooks)
def create_books(create_b: schemas_books.CreateBooks, db: Session = Depends(db_session)):
    db_book_title = crud_books.books_title(db, create_b.title)
    if db_book_title:
        raise HTTPException(
            status_code=400,
            detail="Books title exists"
        )
    return crud_books.create_book(db=db, create_books=create_b)