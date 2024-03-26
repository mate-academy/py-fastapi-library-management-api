from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=book.author_id)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = Query(0, alias="skip"), limit: int = Query(10, alias="limit"), db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = Query(0, alias="skip"), limit: int = Query(10, alias="limit"), db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books", response_model=List[schemas.Book])
def read_books_by_author(author_id: int, skip: int = Query(0, alias="skip"), limit: int = Query(10, alias="limit"), db: Session = Depends(get_db)):
    return crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
