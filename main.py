from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/")
def read_authors(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 5):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Annotated[Session, Depends(get_db)]):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.get("/books/")
def read_books(
    db: Annotated[Session, Depends(get_db)],
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 5,
):
    return crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(
    book_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    return crud.create_book(db=db, book=book)
