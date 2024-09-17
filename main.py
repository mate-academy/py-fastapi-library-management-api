from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/author/", response_model=list[schemas.AuthorGet])
def read_author(db: Session = Depends(get_db)):
    return crud.get_author(db=db)


@app.get("/author/{author_id}/", response_model=schemas.AuthorGet)
def read_one_author(
        author_id: int,
        db: Session = Depends(get_db),
):
    db_author = crud.get_one_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/author/", response_model=schemas.AuthorGet)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author a already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.BookGet])
def read_book(
        author_id: int | None = None,
        db: Session = Depends(get_db),
):
    db_book = crud.get_book(db=db, author_id=author_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/book/", response_model=schemas.BookGet)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_book = crud.get_author_by_id(db=db, author_id=book.author_id)

    if db_book is None:
        raise HTTPException(
            status_code=400,
            detail=f"Author with id {book.author_id} is not exists"
        )

    return crud.create_book(db=db, book=book)
