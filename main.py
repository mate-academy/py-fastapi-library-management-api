from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud import get_all_authors, create_author, get_author_by_name, get_all_books, get_author_by_id, create_book, \
    get_book_by_name, get_author_books
from database import SessionLocal


#Сінглтон сессії бази даних
app = FastAPI()
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}

@app.post("/authors", response_model=schemas.Author)
def create_new_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")
    return create_author(db, author)


#Перший параметр - ендпоінт, другий - те що ми очікуємо отримати після виконання запиту
@app.get("/authors", response_model=list[schemas.Author])
def get_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return get_all_authors(db, skip, limit)

@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author_by_id(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/books", response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = get_book_by_name(db, book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already registered")
    return create_book(db, book)


@app.get("/books", response_model=list[schemas.Book])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return get_all_books(db, skip, limit)

@app.get("/authors/{author_id}/books", response_model=list[schemas.Book])
def get_books_by_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return get_author_books(db, author_id)



