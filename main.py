from typing import List, Optional

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query
)
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, engine
from models import Base
import models


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    version="1.0.0"
)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()




@app.post(
  "/authors/",
  response_model=schemas.AuthorResponse,
  status_code=201
)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
  db_author = (
      db.query(
        models.Author
      ).filter(
        models.Author.name == author.name
      ).first()
  )
  if db_author:
      raise HTTPException(
        status_code=400,
        detail="Author with this name already exists"
    )
  return crud.create_author(db=db, author=author)


@app.get(
  "/authors/",
  response_model=List[schemas.AuthorResponse]
)
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
  authors = crud.get_authors(db, skip=skip, limit=limit)
  return authors


@app.get(
  "/authors/{author_id}",
  response_model=schemas.AuthorResponse
)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
  db_author = crud.get_author(db, author_id=author_id)
  if db_author is None:
    raise HTTPException(
      status_code=404,
      detail="Author not found"
    )
  return db_author




@app.post(
  "/books/",
  response_model=schemas.BookResponse,
  status_code=201
)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
  db_author = crud.get_author(db, author_id=book.author_id)
  if not db_author:
    raise HTTPException(
      status_code=404,
      detail="Author not found"
    )
  return crud.create_book(db=db, book=book)


@app.get(
  "/books/",
  response_model=List[schemas.BookResponse]
)
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = Query(
      None,
      description="Filter books by author ID"
    ),
    db: Session = Depends(get_db),
):
  books = crud.get_books(
    db,
    skip=skip,
    limit=limit,
    author_id=author_id
  )
  return books
