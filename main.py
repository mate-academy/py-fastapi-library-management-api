from typing import Annotated, Any

from fastapi import FastAPI, Depends, Query
from sqlmodel import Session
from database import SessionLocal
from models import create_db_and_tables
from shemas import Book, BookCreate, Author, AuthorCreate
import crud

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.on_event('startup')
def on_startup() -> None:
    create_db_and_tables()


@app.get('/books/', response_model=list[Book])
def show_all_books(
        page: int = 1,
        limit: Annotated[int, Query(le=2)] = 2,
        db: Session = Depends(get_db)
) -> Any:
    return crud.get_books(db, limit=limit, page=page)


@app.get('/books/{book_id}', response_model=Book)
def show_one_book(book_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.get_book(db, book_id)


@app.get('/books/by-author/{author_id}', response_model=list[Book])
def show_books_by_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.get_books_by_author(db, author_id)


@app.post('/books/', response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)) -> Any:
    return crud.create_book(db, book)


@app.get('/authors/', response_model=list[Author])
def show_all_authors(
        page: int = 1,
        limit: Annotated[int, Query(le=2)] = 2,
        db: Session = Depends(get_db)
) -> Any:
    return crud.get_authors(db, limit=limit, page=page)


@app.get('/authors/{author_id}', response_model=Author)
def show_one_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.get_author(db, author_id)


@app.post('/authors/', response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)) -> Any:
    return crud.create_author(db, author)
