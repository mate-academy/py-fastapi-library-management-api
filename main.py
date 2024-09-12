from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import crud
from . import schemas
from .database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hi": "There"}


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/author/", response_model=List[schemas.Author])
def retrieve_author_list(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def retrieve_author(
        author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(author_id=author_id, db=db)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Not found author with id {author_id}"
        )
    return db_author


@app.post("/author/{author_id}/book/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book_for_author(db=db, book=book, author_id=author_id)


@app.get("/book/", response_model=List[schemas.Book])
def retrieve_book_list(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/book/", response_model=schemas.Book)
def filter_books_by_author(
        author_id: int = None, db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_books_by_author(db=db, author_id=author_id)
