from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> list[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_single_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> list[schemas.Book]:
    return crud.get_book_list(db=db, skip=skip, limit=limit)


@app.get(
    "/authors/{author_id}/books/", response_model=list[schemas.Book]
)
def read_books_by_author(
        author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Book]:
    db_author = crud.get_single_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db_books = (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return db_books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(
        book_id: int, db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_single_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404, detail="Book not found"
        )

    return db_book


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
        book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)
