from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from library import models, schemas, crud
from library.database import engine
from library.database import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/authors/{author_id}/books", response_model=list[schemas.BookRead])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_books(db, author_id=author_id)


@app.post("/books/", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db, book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_book


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(skip: int = 0, limit: int = 100, author_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)


@app.get("/books/{book_id}", response_model=schemas.BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
