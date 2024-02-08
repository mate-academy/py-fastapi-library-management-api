from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/author/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_user = crud.get_author_by_name(db, name=author.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Author already registered.")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_author_book(db=db, book=book)


@app.get("/books/", response_model=schemas.Book)
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/?author_id={author_id}/", response_model=schemas.Book)
def read_book_by_author_id(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author_id(db, author_id=author_id)
    return books
