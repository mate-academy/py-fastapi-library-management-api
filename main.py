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


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
) -> list[schemas.Author]:
    authors = crud.get_all_authors(db=db)
    return authors[skip : skip + limit]


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404, detail="There is no author with this id"
        )

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with such name is already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 20,
    author_id: int = None,
    db: Session = Depends(get_db),
) -> list[schemas.Book]:
    books = crud.get_books_list(db=db, author_id=author_id)
    return books[skip : skip + limit]


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)
