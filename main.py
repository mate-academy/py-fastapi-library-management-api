from typing import List

from fastapi import FastAPI, Depends

from crud import read_authors, retrieve_author, delete_author, create_author, update_author, read_books, delete_book, \
    create_book, update_book, retrieve_book
from database import SessionLocal, get_db
from schemas import AuthorRead, AuthorCreate, AuthorUpdate, BookRead, BookCreate, BookUpdate

app = FastAPI()


@app.get("/authors/", response_model=List[AuthorRead])
def list_authors(skip: int = None, limit: int = None, db: SessionLocal = Depends(get_db)):
    return read_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=AuthorRead)
def detail_author(author_id: int, db: SessionLocal = Depends(get_db)):
    return retrieve_author(db, author_id=author_id)


@app.delete("/authors/{author_id}/", status_code=204)
def remove_author(author_id: int, db: SessionLocal = Depends(get_db)):
    return delete_author(db, author_id=author_id)


@app.post("/authors/", response_model=AuthorRead)
def add_author(author: AuthorCreate, db: SessionLocal = Depends(get_db)):
    return create_author(db, author_data=author)


@app.patch("/authors/{author_id}/", response_model=AuthorRead)
def refresh_author(author: AuthorUpdate, author_id: int, db: SessionLocal = Depends(get_db)):
    return update_author(db, author_data=author, author_id=author_id)


@app.get("/books/", response_model=List[BookRead])
def list_books(skip: int = None, limit: int = None, db: SessionLocal = Depends(get_db)):
    return read_books(db, skip, limit)


@app.get("/books/{book_id}/", response_model=BookRead)
def detail_book(book_id: int, db: SessionLocal = Depends(get_db)):
    return retrieve_book(db, book_id=book_id)


@app.delete("/books/{book_id}/", status_code=204)
def remove_book(book_id: int, db: SessionLocal = Depends(get_db)):
    return delete_book(db, book_id=book_id)


@app.post("/books/", response_model=BookRead)
def add_book(book: BookCreate, db: SessionLocal = Depends(get_db)):
    return create_book(db, book_data=book)


@app.patch("/books/{book_id}/", response_model=BookRead)
def refresh_book(book: BookUpdate, book_id: int, db: SessionLocal = Depends(get_db)):
    return update_book(db, book_data=book, book_id=book_id)
