from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id/}", response_model=schemas.AuthorList)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_book(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id/}", response_model=schemas.BookList)
def read_single_book(author_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_author_id(db=db, author_id=author_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
