from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}


@app.get("/books/", response_model=schemas.PaginatedBooks)
def read_books(author_id: int = None, skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    books = crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)
    total = crud.get_book_count(db=db)
    return schemas.PaginatedBooks(total=total, items=books)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=schemas.PaginatedAuthors)
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    total = crud.get_author_count(db=db)
    return schemas.PaginatedAuthors(total=total, items=authors)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author
