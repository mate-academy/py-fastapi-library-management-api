from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/create/", response_model=schemas.Author)
def create_authors(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors_with_pagination(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records per page"),
    db: Session = Depends(get_db),
):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_authors(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.BookCreate)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author does not exist")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def get_authors_with_pagination(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records per page"),
    author_id: int = None,
    db: Session = Depends(get_db),
):
    books = crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)

    if books is None:
        raise HTTPException(status_code=404, detail="Books  not found")
    return books
