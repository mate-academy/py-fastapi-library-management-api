from __future__ import annotations
from typing import Union, List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=List[schemas.Author])
def get_author(
    skip: int = 0, limit: int = 100, book_service: crud.BookService = Depends()
):
    return book_service.get_all_author(skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, book_service: crud.BookService = Depends()
):

    return book_service.create_author(author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: Union[int, None] = None, book_service: crud.BookService = Depends()
):
    db_author = book_service.get_author(author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
    author_id: Union[int, None] = None,
    skip: int = 0,
    limit: int = 100,
    book_service: crud.BookService = Depends(),
):
    return book_service.get_books(author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_author(book: schemas.BookCreate, book_service: crud.BookService = Depends()):

    return book_service.create_book(book=book)
