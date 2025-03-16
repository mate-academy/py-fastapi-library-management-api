from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from database import session
from schemas import (
    AuthorResponseSchema,
    AuthorRequestSchema,
    BookResponseSchema,
    BookRequestSchema,
    DetailBookResponseSchema
)
import crud


app = FastAPI(
    title="LibraryApi"
)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[AuthorResponseSchema])
def get_authors(
        page: int = Query(ge=1, default=1),
        per_page: int = Query(ge=1, le=5, default=3),
        db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db, page, per_page)
    return authors


@app.post("/authors/", response_model=AuthorResponseSchema)
def create_author(
        data: AuthorRequestSchema,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_author(db, data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The author with this name already exists!"
        )


@app.get("/authors/{author_id}/", response_model=AuthorResponseSchema)
def get_single_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found."
        )
    return author


@app.get("/books/", response_model=list[BookResponseSchema])
def get_books(
        page: int = Query(ge=1, default=1),
        per_page: int = Query(ge=1, le=5, default=3),
        author_id: int = Query(default=None),
        db: Session = Depends(get_db)
):
    books = crud.get_all_books(db, page, per_page, author_id)
    return books


@app.post("/books/", response_model=BookResponseSchema)
def create_book(
        data: BookRequestSchema,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_book(db, data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The book with this title already exists!"
        )


@app.get("/books/{book_id}/", response_model=DetailBookResponseSchema)
def get_single_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found."
        )
    return book
