from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors/",
    response_model=schemas.AuthorResponse,
    status_code=201,
)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get(
    "/authors/{author_id}",
    response_model=schemas.AuthorResponse,
)
def read_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author(db, author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookResponse,
    status_code=201,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_book = crud.create_book(db, book, author_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return db_book


@app.get(
    "/books/",
    response_model=list[schemas.BookResponse],
)
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
