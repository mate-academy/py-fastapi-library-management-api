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
def read_all_authors(db: Session = Depends(get_db)) -> list[schemas.Author]:
    return crud.get_all_authors(db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int, db: Session = Depends(get_db)
) -> list[schemas.Author]:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, author_name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists!"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_all_books(
    db: Session = Depends(get_db), author: str | None = None
) -> list[schemas.Book]:
    return crud.get_all_books(db=db, author=author)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(
        book_id: int,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not foundM")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book_by_title_and_author(
        db=db, book_title=book.title, author_id=book.author_id
    )
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="This author has a book with this title already!"
        )

    return crud.create_book(db=db, book=book)


@app.get("/books/author/{author_id}/", response_model=list[schemas.Book])
def read_books_by_author_id(
    author_id: int, db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_books_by_author_id(db=db, author_id=author_id)
