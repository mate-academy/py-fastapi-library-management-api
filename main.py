from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10,
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(
    db: Annotated[Session, Depends(get_db)],
    author: schemas.AuthorCreate,
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    db: Annotated[Session, Depends(get_db)], author_id: int
):
    db_author = crud.get_author_by_id(author_id=author_id, db=db)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book, status_code=201)
def create_book(
    db: Annotated[Session, Depends(get_db)], book: schemas.BookCreate
):
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    if author_id is not None:
        author_db = crud.get_author_by_id(db=db, author_id=author_id)
        if author_db is None:
            raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
