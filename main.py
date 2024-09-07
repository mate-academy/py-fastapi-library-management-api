from typing import List, Dict

from fastapi import FastAPI, Depends, status
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
def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get("/authors/", response_model=List[schemas.Author], status_code=status.HTTP_200_OK)
def get_authors(
        skip: int | None = 0,
        limit: int | None = 10,
        db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author, status_code=status.HTTP_200_OK)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post("/authors/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list[schemas.Book], status_code=status.HTTP_200_OK)
def get_book_by_author_id(author_id: int, db: Session = Depends(get_db)) -> List[schemas.Book]:
    return crud.get_all_books(author_id=author_id, db=db)


@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)
