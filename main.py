from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal

import db.models
import schemas
import crud

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World!"}

# Author

@app.post("/author_create/", response_model=schemas.Author)
def create_new_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_new_author = crud.get_author_by_name(db=db, name=author.name)

    if db_new_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exist!"
        )
    return crud.author_create(db=db, author=author)


@app.get("/authors_list/", response_model=list[schemas.Author])
def get_authors_list(
    limit: int | None = None,
    skip: int | None = None,
    db: Session = Depends(get_db)  
):
    return crud.get_author_list(db=db, limit=limit, skip=skip)


@app.get("/author_by_id/", response_model=schemas.Author)
def get_author_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    return crud.get_author_by_id(db=db, id=id)


# Book

@app.post("/create_book_for_author/", response_model=schemas.Book)
def create_book_for_author(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    db_new_book = crud.get_author_by_id(db=db, id=book.author_id)

    if db_new_book is None:
        raise HTTPException(
            status_code=404,
            detail="Author do not exist!"
        )
    return crud.book_create(db=db, book=book)


@app.get("/books_list/", response_model=list[schemas.Book])
def get_books_list(
    limit: int | None = None,
    skip: int | None = None,
    db: Session = Depends(get_db)  
):
    return crud.get_book_list(db=db, limit=limit, skip=skip)


@app.get("/filter_books_by_author_id/", response_model=list[schemas.Book])
def filter_dooks_by_author_id(
    author_id: int,
    db: Session = Depends(get_db)
):
    db_books = crud.get_author_by_id(db=db, id=author_id)
    
    if db_books is None:
        raise HTTPException(
            status_code=404,
            detail="Author do not exist!"
        )
    return crud.get_book_by_author_id(db=db, author_id=author_id)
