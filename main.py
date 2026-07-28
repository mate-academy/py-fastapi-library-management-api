from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_author(db, author)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists.",
        ) from exc


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorWithBooks)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return db_author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookRead,
    status_code=201,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    if author_id is not None and crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
