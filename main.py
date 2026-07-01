from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from exceptions import AuthorNotFound, AuthorAlreadyExists, BookNotFound
from schemas import (
    AuthorCreate, AuthorUpdate,
    AuthorResponse, BookCreate,
    BookUpdate, BookResponse
)
from db.database import SessionLocal, init_db


init_db()
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=List[AuthorResponse])
def get_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)) -> list[AuthorResponse]:
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/id/{author_id}", response_model=AuthorResponse)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)) -> AuthorResponse:
    try:
        return crud.get_author_by_id(db, author_id)
    except AuthorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/authors/name/{author_name}", response_model=AuthorResponse)
def get_author_by_name(
        author_name: str,
        db: Session = Depends(get_db)) -> AuthorResponse:
    try:
        return crud.get_author_by_name(db, author_name)
    except AuthorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/authors", response_model=AuthorResponse)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)) -> AuthorResponse:
    try:
        return crud.create_author(db, author)
    except AuthorAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/authors/{author_id}", response_model=AuthorResponse)
def update_author(
        author_id: int,
        author: AuthorUpdate,
        db: Session = Depends(get_db)) -> AuthorResponse:
    try:
        return crud.update_author(db, author_id, author)
    except AuthorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/books", response_model=List[BookResponse])
def get_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)) -> List[BookResponse]:
    return crud.get_all_books(db, skip, limit)


@app.get("/books/author/{author_id}", response_model=List[BookResponse])
def get_books_by_author(
        author_id: int,
        db: Session = Depends(get_db)) -> List[BookResponse]:
    return crud.get_books_by_author(db, author_id)


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_by_id(
        book_id: int,
        db: Session = Depends(get_db)):
    try:
        return crud.get_book_by_id(db, book_id)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/books", response_model=BookResponse)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db)) -> BookResponse:
    try:
        return crud.create_book(db, book)
    except AuthorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
        book_id: int,
        book: BookUpdate,
        db: Session = Depends(get_db)) -> BookResponse:
    try:
        return crud.update_book(db, book_id, book)
    except BookNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
