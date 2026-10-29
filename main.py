from collections.abc import Generator

from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hi there!"}


@app.get("/books/")
def get_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_books(
        db=db,
        skip=skip,
        limit=limit,
    )


@app.get("/books/{author_id}/")
def get_books_by_author_id(
    author_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_books_by_author_id(
        db=db,
        author_id=author_id,
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(
        db=db,
        id=book.author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return crud.create_book(db=db, book=book)


@app.get("/authors/")
def get_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_authors(
        db=db,
        skip=skip,
        limit=limit,
    )


@app.get("/authors/{author_id}/")
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)
