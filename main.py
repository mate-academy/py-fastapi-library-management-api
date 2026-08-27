from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> models.Author:
    if crud.get_author_by_name(db, author.name):
        raise HTTPException(status_code=400, detail="Author name already registered")
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[models.Author]:
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> models.Author:
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
) -> models.Book:
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    author_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
) -> list[models.Book]:
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
