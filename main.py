from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


@app.post(
    "/authors/", response_model=schemas.AuthorRead, status_code=201
)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing = crud.get_author_by_name(db, name=author.name)
    if existing:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorRead])
def list_authors(skip: int = 0, limit: int = 100,
                 db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookRead,
    status_code=201,
)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book_for_author(db, author_id=author_id, book=book)


@app.get("/books/", response_model=List[schemas.BookRead])
def list_books(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
