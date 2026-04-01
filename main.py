from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import schemas
from crud import get_all_authors
from db.database import SessionLocal

app = FastAPI()


def get_db() ->Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=201)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_author(db=db, author=author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists",
        )

@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_author(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 3,
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author= crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author

@app.post("/authors/{author_id}/books", response_model=schemas.BookRead)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db, book, author_id)

@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )
