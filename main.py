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


@app.get("/authors/", response_model=list[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.get("/skip_authors/", response_model=list[schemas.Author])
def get_skip_authors(skip_value: int, db: Session = Depends(get_db)):
    return crud.get_skip_authors(db, skip_value)


@app.get("/limit_authors/", response_model=list[schemas.Author])
def get_limit_authors(limit_value: int, db: Session = Depends(get_db)):
    return crud.get_limit_authors(db, limit_value)


@app.get("/author/", response_model=schemas.Author)
def get_author_by_name(author_name: str, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, author_name)
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail="Incorrect author's name"
        )
    else:
        return db_author


@app.post("/create_author/", response_model=schemas.Author)
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


@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)


@app.get("/skip_books/", response_model=list[schemas.Book])
def get_skip_books(skip_value: int, db: Session = Depends(get_db)):
    return crud.get_skip_books(skip_value, db)


@app.get("/limit_books/", response_model=list[schemas.Book])
def get_limit_books(limit_value: int, db: Session = Depends(get_db)):
    return crud.get_limit_books(limit_value, db)


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


@app.post("/create_book/", response_model=schemas.Book)
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
