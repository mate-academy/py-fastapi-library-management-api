from fastapi import FastAPI, Depends
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
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_all_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def single_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_single_author(db=db, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_all_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_single_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_book_by_id(db=db, book_id=book_id)


@app.post("/books/", response_model=schemas.BookCreate)
def book_create(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

