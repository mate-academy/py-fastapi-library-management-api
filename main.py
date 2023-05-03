from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import Author, AuthorCreate, Book, BookCreate, BookCreateForAuthor

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.get("/authors/{author_id}", response_model=Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)


@app.get("/authors/{author_id}/books", response_model=list[Book])
def get_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_books_by_author_id(db=db, author_id=author_id)


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.post("/authors/{author_id}/books", response_model=Book)
def create_book_for_author(author_id: int, book: BookCreateForAuthor, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book_for_author(db=db, author_id=author_id, book=book)

