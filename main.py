from fastapi import FastAPI, Depends, Query
from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from crud import get_author_from_db, get_all_books, create_book_db
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get(path="/")
def index():
    return {"message": "Hello World!"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
):
    authors = crud.get_all_authors(skip=skip, limit=limit, db=db)
    return authors


@app.get(path="/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_from_db(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(path="/authors/", response_model=schemas.Author)
def create_author_endpoint(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author_db(author=author, db=db)


@app.get(path="/books/", response_model=list[schemas.Book])
def get_books_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    author_id: int = Query(None, gt=0),
    db: Session = Depends(get_db),
):
    return get_all_books(skip=skip, limit=limit, db=db, author_id=author_id)


@app.post(path="/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return create_book_db(db=db, book=book)
