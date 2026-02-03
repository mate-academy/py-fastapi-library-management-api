from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors",
    response_model=schemas.AuthorRead,
    status_code=status.HTTP_201_CREATED,
)
def create_author(author_in: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing = crud.get_author_by_name(db, author_in.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists.",
        )
    return crud.create_author(db, author_in)


@app.get("/authors", response_model=list[schemas.AuthorRead])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return author


@app.post(
    "/authors/{author_id}/books",
    response_model=schemas.BookRead,
    status_code=status.HTTP_201_CREATED,
)
def create_book_for_author(
    author_id: int,
    book_in: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.create_book_for_author(db, author_id=author_id, book_in=book_in)


@app.get("/books", response_model=list[schemas.BookRead])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
