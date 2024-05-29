from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import schemas

from app.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def get_all_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
        ):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def get_all_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
        ):

    return crud.get_all_books(
        db, skip=skip, limit=limit
    )


@app.get("/books/by_author/", response_model=List[schemas.Book])
def get_book_by_author(
        skip: int = 0,
        limit: int = 10,
        author_id: int = None,
        db: Session = Depends(get_db)
        ):

    return (
        crud.get_books_by_author(
            db, author_id=author_id,
            skip=skip,
            limit=limit
        )
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
        ):

    return crud.create_book(db=db, book=book)
