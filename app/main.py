from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal, Base, engine
from app.models import DBAuthor, DBBook

app = FastAPI()

# Створення таблиць у БД (якщо їх ще немає)
Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


# --- Автори ---


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = db.query(DBAuthor).offset(skip).limit(limit).all()
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


# --- Книги ---


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Перевірка, чи існує автор
    author = crud.get_author(db=db, author_id=book.author_id)
    if author is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_name: Optional[str] = Query(None, description="Filter books by author name"),
    db: Session = Depends(get_db),
):
    if author_name:
        books = crud.get_book_list(db=db, author_name=author_name)
        # пагінацію застосуємо вручну
        return books[skip : skip + limit]
    else:
        books = db.query(DBBook).offset(skip).limit(limit).all()
        return books