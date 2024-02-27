from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/all_authors/", response_model=list[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors_with_skip_limit(skip_value: int = 0, limit_value: int = 0, db: Session = Depends(get_db)):
    return crud.get_authors_with_skip_limit(db, skip_value, limit_value)


@app.get("/author/", response_model=schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id)
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail="Incorrect author's id"
        )
    else:
        return db_author


@app.post("/author/", response_model=schemas.Author)
def create_author(new_author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if new_author.name == "":
        raise HTTPException(
            status_code=400,
            detail="Author's name is empty"
        )
    db_author = crud.get_author_by_name(db, new_author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )
    return crud.create_author(db, new_author)


@app.get("/all_books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)


@app.get("/books/", response_model=list[schemas.Book])
def get_books_with_skip_limit(skip_value: int = 0, limit_value: int = 0, db: Session = Depends(get_db)):
    return crud.get_books_with_skip_limit(skip_value, limit_value, db)


@app.get("/books_by_author_id/", response_model=list[schemas.Book])
def get_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(author_id, db)


@app.get("/book/", response_model=schemas.Book)
def get_book_by_title(book_title: str, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, book_title)
    if not db_book:
        raise HTTPException(
            status_code=400,
            detail="Incorrect book's title"
        )
    else:
        return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(new_book: schemas.BookCreate, db: Session = Depends(get_db)):
    if new_book.title == "":
        raise HTTPException(
            status_code=400,
            detail="Book title is empty"
        )
    db_book = crud.get_book_by_title(db, new_book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book with the same title already exists"
        )
    return crud.create_book(db, new_book)
