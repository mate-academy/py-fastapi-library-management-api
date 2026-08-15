from typing import Annotated, Generator, Sequence

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine
from models import DBAuthor, DBBook

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(engine)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Annotated[Session, Depends(get_db)]) -> DBAuthor:
    author = crud.get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> Sequence[DBAuthor]:
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
) -> DBAuthor:
    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = Query(None),
) -> Sequence[DBBook]:
    return crud.get_all_books(db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> DBBook:
    author = crud.get_author_by_id(db, book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book)