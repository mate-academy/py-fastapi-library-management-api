from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.models import Base
from schemas import Author, AuthorCreate, Book, BookCreate
from crud import (
    create_author,
    create_book,
    get_authors,
    get_author_by_id,
    get_books,
    get_books_by_author
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_new_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)


@app.get("/authors/", response_model=list[Author])
def read_authors(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=Book)
def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)


@app.get("/books/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db, skip=skip, limit=limit)


@app.get("/books/by_author/{author_id}/", response_model=list[Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return get_books_by_author(db, author_id=author_id)
