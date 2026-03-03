from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, engine
from models import Base


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


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    db: Annotated[Session, Depends(get_db)], author: schemas.AuthorCreate
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    return crud.get_books_list(db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate,
                db: Annotated[Session, Depends(get_db)]):
    if not crud.get_author_by_id(db, author_id=book.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)
