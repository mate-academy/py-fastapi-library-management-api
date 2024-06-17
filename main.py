from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Generator
from database import SessionLocal
import crud
import schemas


app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Author]:
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author was not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
        author_id: int = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_book_list(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)) -> schemas.Book:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book was not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.Book:
    return crud.create_book(db=db, book=book)
