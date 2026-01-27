from typing import List, Optional

from sqlmodel import select

from fastapi import APIRouter, Query, HTTPException, status

from database import SessionDep

from models import Book

from schemas import BookUpdate, BookCreate


router = APIRouter()

@router.post("/books/", response_model=Book)
def create_book(book_data: BookCreate, session: SessionDep) -> Book:
    book = Book(**book_data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/books/", response_model=List[Book])
def read_books(
        session: SessionDep,

        # Pagination
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),

        # Filtering
        author_id: Optional[int] = Query(None),
) -> List[Book]:

    statement = select(Book)

    if author_id:
        statement = statement.where(Book.author_id == author_id)

    statement = statement.offset(offset).limit(limit)

    return session.exec(statement).all()


@router.put("/books/{book_id}", response_model=Book)
def update_book(
        book_id: int,
        book_data: BookUpdate,
        session: SessionDep,
) -> Book:
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    session.commit()
    session.refresh(book)
    return book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_book(
        book_id: int,
        session: SessionDep,
) -> None:

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()
