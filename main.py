from typing import Any, Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import joinedload, Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    name: Annotated[str | None, Query(max_length=30)] = None,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    return crud.get_authors(name=name, db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    title: Annotated[str | None, Query(max_length=60)] = None,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    return crud.get_books(title=title, db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)
):
    books = crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    return books
