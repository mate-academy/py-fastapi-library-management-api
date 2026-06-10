from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import BookCreate, AuthorCreate, Book, Author
import crud


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/")
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.post("/authors/{author_id}/books")
def create_book(author_id: int, book: BookCreate, db: Session = Depends(get_db)):
    book.author_id = author_id
    return crud.create_book(db, book=book)


@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/authors/")
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.post("/authors/")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author=author)


@app.get("/authors/{author_id}")
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
