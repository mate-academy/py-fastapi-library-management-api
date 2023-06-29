from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# uvicorn main:app --reload // command for run server
# alembic revision --autogenerate -m "Initial migrate" // create migration
#  alembic upgrade head // run migration


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_authors(db=db)[skip: skip + limit]


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def author_create(
        author: schemas.AuthorBaseCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such an author already exists",
        )
    return crud.create_author(db=db, author=author)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookBaseCreate, db: Session = Depends(get_db)
):
    return crud.create_book_for_author(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_boos(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_books(db=db, author_id=author_id)[skip: skip + limit]
