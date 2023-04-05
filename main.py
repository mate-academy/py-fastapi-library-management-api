from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db=db, author_id=author_id)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        author_id: int = None
):
    if author_id:
        return crud.get_books_by_author_id(db=db, author_id=author_id)
    return crud.get_books_list(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
