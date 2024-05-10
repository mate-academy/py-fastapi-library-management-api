import uvicorn

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

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


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> list[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def get_author_by_id(
    author_id: int,
    db: Session = Depends(get_db)
) -> schemas.Author:
    db_author_id = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author_id is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return db_author_id


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book with such title already exists"
        )

    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(
            status_code=400,
            detail="Such author was not found, "
                   "please indicate an existing author"
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def get_books_by_author_id(
        author_id: int = None,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_books_by_author_id(db=db, author_id=author_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
