from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

library = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@library.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
        skip: int,
        limit: int,
        db: Session = Depends(get_db)
) -> Session:
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@library.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@library.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exists in db"
        )

    return crud.create_author(db=db, author=author)


@library.get("/books/", response_model=list[schemas.BookList])
def read_books(
        skip: int,
        limit: int,
        db: Session = Depends(get_db)
) -> Session:
    return crud.get_book_list(db=db, skip=skip, limit=limit)


@library.post("/books/", response_model=schemas.BookList)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
