from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crud import add_book, select_author_books
from database import get_session
from schemas import BookCreateSchema, BookResponseSchema, BookListSchema

books_router = APIRouter()


@books_router.post(
    path="/books/",
    response_model=BookResponseSchema,
    description="Create a new book for a specific author.",
    status_code=201,
)
def create_book(
        book_data: BookCreateSchema,
        db: Session = Depends(get_session),

):
    return BookResponseSchema.model_validate(add_book(db, book_data))


@books_router.get(
    path="/books/",
    response_model=BookListSchema,
    description="Retrieve a list of books with pagination (skip, limit).",
    summary="Filter books by author ID.",
    status_code=200
)
def get_books(
        author: int | None = Query(),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        db: Session = Depends(get_session),
):

    return BookListSchema(books=select_author_books(db, skip, limit, author))
